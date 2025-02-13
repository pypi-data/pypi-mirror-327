import random
import os

import cv2
import numpy as np
import pickle
from scipy.ndimage import gaussian_filter
from scipy.spatial.distance import mahalanobis
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
from tqdm import tqdm

from ai.DTO import FeatureExtraction
from ai.feature_extraction import FeatureExtractor
from config.DTO import PadimADConfig
from data.transform import DataTransform


class PadimAnomalyDetector:

    train_outputs = None
    cal_min_score = -1  # detected minimum score on the calibrated data
    cal_max_score = -1  # detected maximum score on the calibrated data

    """
    central class for managing to create, load, run and use anomaly detection based on PaDim.
    """
    def __init__(self, config: PadimADConfig):
        """
        default constructor with config for a Padim Anomaly Detector
        :param config:
        """
        self.config = config
        self.feat_extractor = FeatureExtractor(
            model_name=config.model_name,
            device=config.device,
        )
        # TODO debug statement to check results for repeatability
        random.seed(1024)
        torch.manual_seed(1024)
        if config.device == 'cuda':
            torch.cuda.manual_seed_all(1024)

    def train_anomaly_detection(self, dataset, progress_bar=None):
        """
        train an anomaly detection on a given dataset, good data without anomalies
        :param dataset: holds the data on which the AD is being tuned for.
        :param progress_bar: if an ui element is involved provide a progress bar to modify
        :return:
        """
        # TODO pickle is broken here!!
        with open('../train_class.pkl', 'rb') as f:
            self.train_outputs = pickle.load(f)
        # return

        train_dataloader = DataLoader(dataset, batch_size=self.config.batch_size, pin_memory=True)
        print('[INFO] extracting features from training dataset: {}'.format(len(dataset)))
        feature_extractions = []

        aux = 0

        for x in tqdm(train_dataloader, total=len(train_dataloader)):
            fe = self.feat_extractor.extract_features(in_sample=x)
            fe.detach_cpu()
            fe.move_to_device('cpu')
            feature_extractions.append(fe)
            if progress_bar is not None:
                step_width = 1 / len(train_dataloader)
                aux += step_width
                progress_bar.set(aux)
            # progress_bar.step()
        fe_summary = FeatureExtraction(
            layer_0=torch.cat([x.layer_0.clone() for x in feature_extractions], dim=0),
            layer_1=torch.cat([x.layer_1.clone() for x in feature_extractions], dim=0),
            layer_2=torch.cat([x.layer_2.clone() for x in feature_extractions], dim=0),
        )
        fe_summary.embed_vectors()

        # randomly select d dimension
        embedding_vectors = torch.index_select(fe_summary.embedded_vectors, 1, self.feat_extractor.idx)
        # calculate multivariate Gaussian distribution
        B, C, H, W = embedding_vectors.size()
        embedding_vectors = embedding_vectors.view(B, C, H * W)
        mean = torch.mean(embedding_vectors, dim=0).numpy()
        cov = torch.zeros(C, C, H * W).numpy()
        I = np.identity(C)
        print('[INFO] creating covariance matrices for each pixel')
        aux = 0
        if progress_bar is not None:
            progress_bar.stop()
            progress_bar.set(0)

        for i in tqdm(range(H * W), total=H * W):
            cov[:, :, i] = np.cov(embedding_vectors[:, :, i].numpy(), rowvar=False) + 0.01 * I

            if progress_bar is not None and i % 100 == 0:
                step_width = 1 / (H * W)
                aux += step_width * 100
                progress_bar.set(aux)

        # save the temporary training outputs on mean and covariance
        self.train_outputs = [mean, cov]
        conv_inv_list = []
        aux = 0
        if progress_bar is not None:
            progress_bar.stop()
            progress_bar.set(0)

        for i in tqdm(range(H * W), total=H * W):
            conv_inv = np.linalg.inv(self.train_outputs[1][:, :, i])
            conv_inv_list.append(conv_inv)

            if progress_bar is not None and i % 100 == 0:
                step_width = 1 / (H * W)
                aux += step_width * 100
                progress_bar.set(aux)

        # conv_inv_list = np.array(conv_inv_list).transpose(1, 0).reshape(C, H * W)
        # save learned distribution
        self.train_outputs = [mean, cov, conv_inv_list]

        with open('../train_class.pkl', 'wb') as f:
            pickle.dump(self.train_outputs, f)
        print('[INFO] finished adjusting padim anomaly detector.')

    def detect_anomaly(self, im, transform, normalize=False):
        """
        detect anomaly on an image.
        :param im: image to detect anomaly on.
        :param transform: transformations to apply to the image being sent
        :param normalize: normalize the output map
        :return:
        """
        with torch.no_grad():
            x_in = transform(im)
            x_in = torch.unsqueeze(x_in, 0)
            fe = self.feat_extractor.extract_features(in_sample=x_in)
            fe.detach_cpu()
            fe.move_to_device('cpu')

        fe.embed_vectors()
        embedding_vectors = torch.index_select(fe.embedded_vectors, 1, self.feat_extractor.idx)

        # calculate distance matrix
        B, C, H, W = embedding_vectors.size()
        embedding_vectors = embedding_vectors.view(B, C, H * W).numpy()
        dist_list = []
        for i in tqdm(range(H * W), total=H * W):
            mean = self.train_outputs[0][:, i]
            # conv_inv = np.linalg.inv(self.train_outputs[1][:, :, i])
            conv_inv = self.train_outputs[2][i]
            dist = [mahalanobis(sample[:, i], mean, conv_inv) for sample in embedding_vectors]
            dist_list.append(dist)

        dist_list = np.array(dist_list).transpose(1, 0).reshape(B, H, W)
        # up-sample
        dist_list = torch.tensor(dist_list)
        score_map = F.interpolate(
            dist_list.unsqueeze(1),
            size=x_in.size(2),
            mode='bilinear',
            align_corners=False
        ).squeeze().numpy()

        # apply gaussian smoothing on the score map
        for i in range(score_map.shape[0]):
            score_map[i] = gaussian_filter(score_map[i], sigma=4)

        # Normalization
        max_score = self.cal_max_score
        min_score = self.cal_min_score
        print('max detected on anomaly: {}, max detected on cal: {}'.format(np.max(score_map), max_score))
        print('min detected on anomaly: {}, min detected on cal: {}'.format(np.min(score_map), min_score))
        max_score = max(self.cal_max_score, np.max(score_map))
        test_score_map = (score_map - min_score) / (max_score - min_score)

        if normalize:
            test_score_map = (test_score_map * 255).astype(np.uint8)
        return test_score_map

    def calibrate_anomalies_on_dataset(self, dataset, progress_bar=None):
        """
        calibrate the anomaly detector on a dataset to extract maximum and minimum score.
        The calibration dataset should not contain any anomalies in it, because that would cause the anomaly detector
        to corrupt.
        :param dataset: validation data to calibrate on
        :param progress_bar: if using the gui, use a progress bar to show the progress to the end user
        :return:
        """
        test_dataloader = DataLoader(dataset, batch_size=self.config.batch_size, pin_memory=True)

        test_images = []
        test_fes = []
        aux = 0
        if progress_bar is not None:
            progress_bar.stop()
            progress_bar.set(0)

        for x in tqdm(test_dataloader, '| feature extraction | test |'):
            test_images.extend(x.cpu().detach().numpy())
            with torch.no_grad():
                fe = self.feat_extractor.extract_features(in_sample=x)
                fe.detach_cpu()
                fe.move_to_device('cpu')
                test_fes.append(fe)

            if progress_bar is not None:
                step_width = 1 / len(test_dataloader)
                aux += step_width
                progress_bar.set(aux)

        fe_summary = FeatureExtraction(
            layer_0=torch.cat([x.layer_0.clone() for x in test_fes], dim=0),
            layer_1=torch.cat([x.layer_1.clone() for x in test_fes], dim=0),
            layer_2=torch.cat([x.layer_2.clone() for x in test_fes], dim=0),
        )
        fe_summary.embed_vectors()
        # randomly select d dimension
        embedding_vectors = torch.index_select(fe_summary.embedded_vectors, 1, self.feat_extractor.idx)

        # calculate distance matrix
        B, C, H, W = embedding_vectors.size()
        embedding_vectors = embedding_vectors.view(B, C, H * W).numpy()
        dist_list = []
        aux = 0
        if progress_bar is not None:
            progress_bar.stop()
            progress_bar.set(0)
        for i in tqdm(range(H * W), total=H * W):
            mean = self.train_outputs[0][:, i]
            # conv_inv = np.linalg.inv(self.train_outputs[1][:, :, i])
            conv_inv = self.train_outputs[2][i]
            dist = [mahalanobis(sample[:, i], mean, conv_inv) for sample in embedding_vectors]
            dist_list.append(dist)

            if progress_bar is not None and i % 100 == 0:
                step_width = 1 / (H * W)
                aux += step_width * 100
                progress_bar.set(aux)

        dist_list = np.array(dist_list).transpose(1, 0).reshape(B, H, W)

        # upsample
        dist_list = torch.tensor(dist_list)
        score_map = F.interpolate(
            dist_list.unsqueeze(1),
            size=x.size(2),
            mode='bilinear',
            align_corners=False
        ).squeeze().numpy()

        # apply gaussian smoothing on the score map
        for i in range(score_map.shape[0]):
            score_map[i] = gaussian_filter(score_map[i], sigma=4)

        # Normalization
        max_score = score_map.max()
        min_score = score_map.min()

        self.cal_max_score = max_score * 2
        self.cal_min_score = min_score

    def detect_anomalies_on_dataset(self, dataset, path: str):
        """
        detect anomalies on an entire dataset
        :param dataset: test-dataset to detect anomalies on.
        :param path: write results into a path
        :return:
        """
        test_dataloader = DataLoader(dataset, batch_size=self.config.batch_size, pin_memory=True)

        test_images = []
        test_fes = []
        for x in tqdm(test_dataloader, '| feature extraction | test |'):
            test_images.extend(x.cpu().detach().numpy())
            with torch.no_grad():
                fe = self.feat_extractor.extract_features(in_sample=x)
                fe.detach_cpu()
                fe.move_to_device('cpu')
                test_fes.append(fe)

        fe_summary = FeatureExtraction(
            layer_0=torch.cat([x.layer_0.clone() for x in test_fes], dim=0),
            layer_1=torch.cat([x.layer_1.clone() for x in test_fes], dim=0),
            layer_2=torch.cat([x.layer_2.clone() for x in test_fes], dim=0),
        )
        fe_summary.embed_vectors()
        # randomly select d dimension
        embedding_vectors = torch.index_select(fe_summary.embedded_vectors, 1, self.feat_extractor.idx)

        # calculate distance matrix
        B, C, H, W = embedding_vectors.size()
        embedding_vectors = embedding_vectors.view(B, C, H * W).numpy()
        dist_list = []
        for i in tqdm(range(H * W), total=H * W):
            mean = self.train_outputs[0][:, i]
            conv_inv = np.linalg.inv(self.train_outputs[1][:, :, i])
            dist = [mahalanobis(sample[:, i], mean, conv_inv) for sample in embedding_vectors]
            dist_list.append(dist)

        dist_list = np.array(dist_list).transpose(1, 0).reshape(B, H, W)

        # upsample
        dist_list = torch.tensor(dist_list)
        score_map = F.interpolate(
            dist_list.unsqueeze(1),
            size=x.size(2),
            mode='bilinear',
            align_corners=False
        ).squeeze().numpy()

        # apply gaussian smoothing on the score map
        for i in range(score_map.shape[0]):
            score_map[i] = gaussian_filter(score_map[i], sigma=4)

        # Normalization
        max_score = self.cal_max_score
        min_score = self.cal_min_score
        scores = (score_map - min_score) / (max_score - min_score)
        score_diff = scores.max() - scores.min()
        threshold = int(0.356 * 255)
        for i in range(len(test_images)):
            origin_im = DataTransform.denormalize_image(test_images[i])
            cv2.imwrite(os.path.join(path, '{:02d}_origin_im.png'.format(i)), origin_im)
            test_score_map = (scores[i] * 255).astype(np.uint8)
            cv2.imwrite(os.path.join(path, '{:02d}_scores.png'.format(i)), test_score_map)
            (T, thresh) = cv2.threshold(test_score_map, threshold, 255, cv2.THRESH_BINARY)
            cv2.imwrite(os.path.join(path, '{:02d}_thresh.png'.format(i)), thresh)

