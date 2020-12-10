import unittest
import numpy as np
import math
import warnings
from sklearn.datasets import make_blobs

import ps6 as ps6

class TestPS6(unittest.TestCase):
    
    
    
    def test_01_prep_dataset(self):
        raw_data = np.random.randint(10, size=(10,100))
        prepped_data = ps6.prep_dataset(raw_data)
        
        self.assertIsInstance(prepped_data, tuple, "Incorrect return type, expected tuple of np arrays")
        self.assertIsInstance(prepped_data[0], np.ndarray, "Incorrect return type, expected tuple of np arrays")
        self.assertIsInstance(prepped_data[1], np.ndarray, "Incorrect return type, expected tuple of np arrays")
        data = prepped_data[0]
        labels = prepped_data[1]
        
        self.assertTrue(data.shape[0] == raw_data.shape[0] and data.shape[1] == raw_data.shape[1]-1, "Incorrect shape for data, expected array of shape (N, # feats)")
        self.assertTrue(labels.size == raw_data.shape[0], "Incorrect shape for labels, expected array of shape (N, 1)")
        
        self.assertTrue(np.array_equal(raw_data[:,1:], data))
        self.assertTrue(np.array_equal(raw_data[:,0], labels))
        
    def test_02_kmeans(self):
        file = "wine.data"
        raw_data = ps6.read_data(file)
        features, labels = ps6.prep_dataset(raw_data)
        k = 3
        result = ps6.kmeans(features, k)
        
        
        self.assertTrue(type(result) == tuple and len(result) == 2)
        
        pred = result[0]
        inertia = result[1]
        
        
        correct_pred = np.array([1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                            1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2,
                            2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 2, 0, 0, 2,
                            0, 0, 2, 2, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0,
                            2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2,
                            0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                            0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 2,
                            2, 2, 0, 2, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2,
                            2, 0], dtype=np.int32)
        correct_inertia = 2370689.686782968
        
        for i in range(k):
            self.assertEqual(np.sum(correct_pred == k), np.sum(pred == k))
        self.assertTrue(math.isclose(inertia, correct_inertia))
    
    def test_03_scale_data(self):
        file = "wine.data"
        raw_data = ps6.read_data(file)
        data, labels = ps6.prep_dataset(raw_data)
        data = ps6.scale_data(data)
        for i in range(data.shape[1]):
            self.assertTrue(math.isclose(max(data[:,i]), 1.0, abs_tol=1e-8))
            self.assertTrue(math.isclose(min(data[:,i]), 0.0, abs_tol=1e-8))
        

    def test_04_cluster_purity(self):
        file = "wine.data"
        raw_data = ps6.read_data(file)
        data, labels = ps6.prep_dataset(raw_data)
        data = ps6.scale_data(data)
        clusters, _ = ps6.kmeans(data, 3)
        result = ps6.cluster_purity(clusters, labels)
        
        correct = set([0.9672, 0.8889, 1.0])
        self.assertIsInstance(result,list)
        result = set(result)
        self.assertTrue(len(result)==3)
        for r in result:
            self.assertTrue(r in correct)
        
        # generated blobs
        x,y = make_blobs(n_samples=[10,15,20,25], n_features=10, random_state=0)
        clusters, _ = ps6.kmeans(x,4)
        result = ps6.cluster_purity(clusters, y)
        correct = [1.0,1.0,1.0]
        for c, r in zip(correct, result):
            self.assertTrue(math.isclose(c,r, abs_tol=1e-4))
        
    
    def test_05_try_k_clusters(self):
        file = "wine.data"
        raw_data = ps6.read_data(file)
        data, labels = ps6.prep_dataset(raw_data)
        data = ps6.scale_data(data)
        k = 10
        purities, inertias = ps6.try_k_clusters(data, labels, k)
        
        self.assertIsInstance(purities, list)
        self.assertIsInstance(inertias, list)
        self.assertEqual(len(purities), len(inertias))
        self.assertTrue(len(purities) == 10)
        
        correct_purities = [0.3989, 0.616, 0.952, 0.9555, 0.9374, 0.889, 0.936, 0.8728, 0.93, 0.9308]
        correct_inertias = [95.5995, 64.5377, 48.954, 44.7693, 42.1437, 40.4269, 37.9266, 36.0972, 34.4839, 33.2094]
        
        for c, r in zip(correct_purities, purities):
            self.assertTrue(math.isclose(c,r, abs_tol=1e-4))
        
        for c, r in zip(correct_inertias, inertias):
            self.assertTrue(math.isclose(c,r, abs_tol=1e-4))
        
        
        
if __name__ == '__main__':
    # Run the tests and print verbose output to stderr.
    warnings.simplefilter('ignore', np.RankWarning)
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS6))
    unittest.TextTestRunner(verbosity=2).run(suite)
