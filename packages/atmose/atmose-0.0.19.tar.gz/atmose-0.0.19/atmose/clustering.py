import pandas as pd
import numpy as np
import umap
import hdbscan
import math
import optuna
import logging
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


class ClusteringEngine:
    def __init__(self, 
        dims=3, 
        min_clusters=3, 
        max_clusters=25, 
        min_noise_ratio=0.03,
        max_noise_ratio=0.35,
        n_trials=20, 
        random_state=42,
        embedding_col_name="embedding_vector",
        
        umap_n_neighbors_min=2,
        umap_n_neighbors_max=25,
        umap_min_dist_min=0.0,
        umap_min_dist_max=0.1,
        umap_spread_min=1.0,
        umap_spread_max=10.0,
        umap_learning_rate_min=0.08,
        umap_learning_rate_max=1.0,
        umap_min_dims=2,
        umap_max_dims=20,
        umap_metric="cosine",
        
        hdbscan_min_cluster_size_multiplier_min=0.005,
        hdbscan_min_cluster_size_multiplier_max=0.025,
        hdbscan_min_samples_min=2,
        hdbscan_min_samples_max=50,
        hdbscan_epsilon_min=0.0,
        hdbscan_epsilon_max=1.0,
        hdbscan_metric="euclidean",
        hdbscan_cluster_selection_method="eom",
        
        optuna_jobs=-1,
        hdbscan_outlier_threshold=20,
        
        target_pca_evr=0.9,
        
        hdbscan_branch_detection=False,
        branch_min_cluster_size_min=5,
        branch_min_cluster_size_max=25,
        branch_selection_persistence_min=0.0,
        branch_selection_persistence_max=0.1,
        branch_label_sides_as_branches=False
    ):
        """
        Initialize the optimizer with UMAP and HDBSCAN hyperparameter settings.

        Args:
            dims (int or None): Number of dimensions for UMAP reduction. If None, a wider search is performed.
            min_clusters (int): Minimum acceptable number of clusters.
            max_clusters (int): Maximum acceptable number of clusters.
            n_trials (int): Number of optimization trials for hyperparameter tuning.
            random_state: Seed for UMAP and PCA to ensure reproducibility.
            embedding_col_name (str): Name of the column containing embedding vectors.
            umap_n_neighbors_min (int): Minimum value for UMAP's n_neighbors parameter.
            umap_n_neighbors_max (int): Maximum value for UMAP's n_neighbors parameter.
            umap_min_dist_min (float): Minimum value for UMAP's min_dist parameter.
            umap_min_dist_max (float): Maximum value for UMAP's min_dist parameter.
            umap_spread_min (float): Minimum value for UMAP's spread parameter.
            umap_spread_max (float): Maximum value for UMAP's spread parameter.
            umap_learning_rate_min (float): Minimum value for UMAP's learning_rate parameter.
            umap_learning_rate_max (float): Maximum value for UMAP's learning_rate parameter.
            umap_min_dims (int): Minimum number of dimensions for UMAP reduction.
            umap_max_dims (int): Maximum number of dimensions for UMAP reduction.
            umap_metric (str): Distance metric to use for UMAP reduction.
            hdbscan_min_cluster_size_multiplier_min (float): Minimum multiplier for HDBSCAN's min_cluster_size.
            hdbscan_min_cluster_size_multiplier_max (float): Maximum multiplier for HDBSCAN's min_cluster_size.
            hdbscan_min_samples_min (int): Minimum value for HDBSCAN's min_samples parameter.
            hdbscan_min_samples_max (int): Maximum value for HDBSCAN's min_samples parameter.
            hdbscan_epsilon_min (float): Minimum value for HDBSCAN's cluster_selection_epsilon parameter.
            hdbscan_epsilon_max (float): Maximum value for HDBSCAN's cluster_selection_epsilon parameter.
            hdbscan_metric (str): Distance metric to use for HDBSCAN clustering.
            hdbscan_cluster_selection_method (str): Method to use for selecting clusters in HDBSCAN.
            optuna_jobs (int): Number of parallel jobs to run during Optuna optimization. Set to -1 for all CPUs.
            hdbscan_outlier_threshold (int): Percentile threshold for HDBSCAN outlier detection.
            min_noise_ratio (float): Minimum acceptable noise ratio (fraction of noise points). Values below this are considered "too good to be true".
            max_noise_ratio (float): Maximum acceptable noise ratio (fraction of noise points). Values above this are considered degenerate.
            target_pca_evr (float or None): Minimum explained variance ratio for PCA preprocessing (default: 0.9).
            hdbscan_branch_detection (bool): Whether to enable branch detection in HDBSCAN. Useful if your silhoutte plot shows "fat" rounded clusters.
            branch_min_cluster_size_min (int): Minimum value for branch detector's min_branch_size.
            branch_min_cluster_size_max (int): Maximum value for branch detector's min_branch_size.
            branch_selection_persistence_min (float): Minimum value for branch detector's branch_selection_persistence.
            branch_selection_persistence_max (float): Maximum value for branch detector's branch_selection_persistence.
            branch_label_sides_as_branches (bool): Default value for label_sides_as_branches; this will be tuned.
            
        """
        # -------------------------------
        # Assign initialization parameters to instance attributes.
        # -------------------------------
        self.dims: int = dims
        self.min_clusters: int = min_clusters
        self.max_clusters: int = max_clusters
        self.n_trials: int = n_trials
        self.random_state: int = random_state
        self.embedding_col_name: str = embedding_col_name
        
        self.umap_n_neighbors_min: int = umap_n_neighbors_min
        self.umap_n_neighbors_max: int = umap_n_neighbors_max
        self.umap_min_dist_min: float = umap_min_dist_min
        self.umap_min_dist_max: float = umap_min_dist_max
        self.umap_spread_min: float = umap_spread_min
        self.umap_spread_max: float = umap_spread_max
        self.umap_learning_rate_min: float = umap_learning_rate_min
        self.umap_learning_rate_max: float = umap_learning_rate_max
        self.umap_min_dims: int = umap_min_dims
        self.umap_max_dims: int = umap_max_dims
        self.umap_metric: str = umap_metric
        
        self.hdbscan_min_cluster_size_multiplier_min: float = hdbscan_min_cluster_size_multiplier_min
        self.hdbscan_min_cluster_size_multiplier_max: float = hdbscan_min_cluster_size_multiplier_max
        self.hdbscan_min_samples_min: int = hdbscan_min_samples_min
        self.hdbscan_min_samples_max: int = hdbscan_min_samples_max
        self.hdbscan_epsilon_min: float = hdbscan_epsilon_min
        self.hdbscan_epsilon_max: float = hdbscan_epsilon_max
        self.hdbscan_metric: str = hdbscan_metric
        self.hdbscan_cluster_selection_method: str = hdbscan_cluster_selection_method
        
        self.optuna_jobs: int = optuna_jobs
        self.hdbscan_outlier_threshold: int = hdbscan_outlier_threshold

        self.min_noise_ratio: float = min_noise_ratio
        self.max_noise_ratio: float = max_noise_ratio

        self.target_pca_evr: float|None = target_pca_evr
        
        self.hdbscan_branch_detection: bool = hdbscan_branch_detection
        self.branch_min_cluster_size_min: int = branch_min_cluster_size_min
        self.branch_min_cluster_size_max: int = branch_min_cluster_size_max
        self.branch_selection_persistence_min: float = branch_selection_persistence_min
        self.branch_selection_persistence_max: float = branch_selection_persistence_max
        self.branch_label_sides_as_branches: bool = branch_label_sides_as_branches

        # -------------------------------
        # Logger Initialization: Create and configure a logger for the ClusteringEngine instance.
        # -------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)

    def _create_models(self, trial, num_data_pts):
        """
        Create UMAP and HDBSCAN models with hyperparameters suggested by the Optuna trial.

        For UMAP, if self.dims is provided (not None), the number of components is fixed to that value.
        Otherwise, the number of components is sampled from the range [umap_min_dims, umap_max_dims].
        Other UMAP hyperparameters (n_neighbors, min_dist, spread, learning_rate) are also sampled within their specified ranges.
        For HDBSCAN, hyperparameters are suggested based on the number of data points, with the min_cluster_size 
        computed as a multiplier of the data count.

        Args:
            trial (optuna.trial.Trial): Optuna trial object to sample hyperparameters.
            num_data_pts (int): Number of data points in the dataset.

        Returns:
            tuple: A tuple containing:
                - umap.UMAP: UMAP model instance with suggested parameters.
                - hdbscan.HDBSCAN: HDBSCAN model instance with suggested parameters.
                - dict: Dictionary of UMAP parameters.
                - dict: Dictionary of HDBSCAN parameters.
        """
        self.logger.debug("Creating models for trial with num_data_pts=%d", num_data_pts)
        # -------------------------------
        # UMAP Parameter Selection:
        # Determine the number of components and suggest hyperparameters using the trial.
        # -------------------------------
        if self.dims is None:
            umap_n_components = trial.suggest_int("umap_n_components", self.umap_min_dims, self.umap_max_dims)
        else:
            umap_n_components = self.dims
            
        umap_params = {
            "n_neighbors": trial.suggest_int("umap_n_neighbors", self.umap_n_neighbors_min, self.umap_n_neighbors_max),
            "min_dist": trial.suggest_float("umap_min_dist", self.umap_min_dist_min, self.umap_min_dist_max),
            "spread": trial.suggest_float("umap_spread", self.umap_spread_min, self.umap_spread_max),
            "metric": self.umap_metric,
            "random_state": self.random_state,
            "learning_rate": trial.suggest_float("umap_learning_rate", self.umap_learning_rate_min, self.umap_learning_rate_max),
            "init": "spectral",
            "n_components": umap_n_components,
        }
        self.logger.debug("UMAP parameters: %s", umap_params)
        
        # -------------------------------
        # HDBSCAN Parameter Selection:
        # Suggest hyperparameters for HDBSCAN based on the number of data points.
        # -------------------------------
        hdbscan_params = {
            "min_cluster_size": trial.suggest_int(
                "hdbscan_min_cluster_size",
                math.ceil(self.hdbscan_min_cluster_size_multiplier_min * num_data_pts),
                math.ceil(self.hdbscan_min_cluster_size_multiplier_max * num_data_pts)
            ),
            "min_samples": trial.suggest_int("hdbscan_min_samples", self.hdbscan_min_samples_min, self.hdbscan_min_samples_max),
            "cluster_selection_epsilon": trial.suggest_float("hdbscan_epsilon", self.hdbscan_epsilon_min, self.hdbscan_epsilon_max),
            "metric": self.hdbscan_metric,
            "cluster_selection_method": self.hdbscan_cluster_selection_method,
            "prediction_data": True
        }
        # Enable branch detection data if the flag is set.
        if self.hdbscan_branch_detection:
            hdbscan_params["branch_detection_data"] = True
            self.logger.debug("Branch detection enabled: adding branch_detection_data=True to HDBSCAN parameters.")
        self.logger.debug("HDBSCAN parameters: %s", hdbscan_params)
        
        # -------------------------------
        # Return the constructed UMAP and HDBSCAN models along with their parameter dictionaries.
        # -------------------------------
        return (
            umap.UMAP(**umap_params),
            hdbscan.HDBSCAN(**hdbscan_params),
            umap_params,
            hdbscan_params,
        )
    
    def _default_models(self, num_data_pts):
        """
        Create UMAP and HDBSCAN models using a set of predefined default hyperparameters.
        This fallback is used when optimization fails to find any valid Pareto-optimal trials.

        Args:
            num_data_pts (int): Number of data points in the dataset.

        Returns:
            tuple: A tuple containing:
                - umap.UMAP: UMAP model instance with default parameters.
                - hdbscan.HDBSCAN: HDBSCAN model instance with default parameters.
                - dict: Dictionary of default UMAP parameters.
                - dict: Dictionary of default HDBSCAN parameters.
        """
        self.logger.debug("Creating default models using predefined hyperparameters for fallback.")
        # -------------------------------
        # Determine default n_components for UMAP.
        # -------------------------------
        umap_n_components = self.dims if self.dims is not None else 3
        
        # -------------------------------
        # Compute default UMAP parameters as the average of the min and max values.
        # -------------------------------
        umap_params = {
            "n_neighbors": (self.umap_n_neighbors_min + self.umap_n_neighbors_max) // 2,
            "min_dist": (self.umap_min_dist_min + self.umap_min_dist_max) / 2,
            "spread": (self.umap_spread_min + self.umap_spread_max) / 2,
            "metric": self.umap_metric,
            "random_state": self.random_state,
            "learning_rate": (self.umap_learning_rate_min + self.umap_learning_rate_max) / 2,
            "init": "spectral",
            "n_components": umap_n_components,
        }
        # -------------------------------
        # Compute default HDBSCAN parameters similarly.
        # -------------------------------
        hdbscan_params = {
            "min_cluster_size": math.ceil(((self.hdbscan_min_cluster_size_multiplier_min + self.hdbscan_min_cluster_size_multiplier_max) / 2) * num_data_pts),
            "min_samples": (self.hdbscan_min_samples_min + self.hdbscan_min_samples_max) // 2,
            "cluster_selection_epsilon": (self.hdbscan_epsilon_min + self.hdbscan_epsilon_max) / 2,
            "metric": self.hdbscan_metric,
            "cluster_selection_method": self.hdbscan_cluster_selection_method,
            "prediction_data": True
        }
        self.logger.debug("Default UMAP parameters: %s", umap_params)
        self.logger.debug("Default HDBSCAN parameters: %s", hdbscan_params)
        
        # -------------------------------
        # Instantiate the UMAP and HDBSCAN models with the default parameters.
        # -------------------------------
        umap_model = umap.UMAP(**umap_params)
        hdbscan_model = hdbscan.HDBSCAN(**hdbscan_params)
        return umap_model, hdbscan_model, umap_params, hdbscan_params

    def _create_branch_params(self, trial):
        """
        Create BranchDetector hyperparameters from the trial.

        Returns:
            dict: Dictionary with branch detection parameters:
                - min_branch_size: int, sampled from self.branch_min_cluster_size_min to self.branch_min_cluster_size_max.
                - branch_selection_persistence: float, sampled from self.branch_selection_persistence_min to self.branch_selection_persistence_max.
                - label_sides_as_branches: bool, sampled from [True, False].
        """
        branch_params = {
            "min_branch_size": trial.suggest_int("branch_min_cluster_size", self.branch_min_cluster_size_min, self.branch_min_cluster_size_max),
            "branch_selection_persistence": trial.suggest_float("branch_selection_persistence", self.branch_selection_persistence_min, self.branch_selection_persistence_max),
            "label_sides_as_branches": trial.suggest_categorical("branch_label_sides_as_branches", [True, False])
        }
        self.logger.debug("BranchDetector parameters: %s", branch_params)
        return branch_params

    def _compute_metrics(self, reduced_data, labels):
        """
        Compute clustering metrics including silhouette score and negative noise ratio.

        This function calculates the silhouette score for non-noise points (where noise is denoted by label -1)
        and computes the negative noise ratio. Returns None if there's only one cluster or too few non-noise points.

        Args:
            reduced_data (np.ndarray): Data after dimensionality reduction.
            labels (np.ndarray): Cluster labels assigned by HDBSCAN (or BranchDetector), with -1 indicating noise.

        Returns:
            dict or None: Dictionary containing 'silhouette' and 'neg_noise' if valid, otherwise None.
        """
        # -------------------------------
        # Identify non-noise points (labels != -1).
        # -------------------------------
        mask = labels != -1
        self.logger.debug("Computed non-noise mask: %s (sum=%d)", mask, np.sum(mask))
        
        # -------------------------------
        # Check if there are enough clusters and non-noise points to compute metrics.
        # -------------------------------
        if len(np.unique(labels)) <= 1 or np.sum(mask) < 2:
            self.logger.debug("Not enough clusters or non-noise points to compute metrics.")
            return None
        
        # -------------------------------
        # Compute the silhouette score for the non-noise data.
        # -------------------------------
        silhouette = silhouette_score(X=reduced_data[mask], labels=labels[mask], metric="euclidean")
        
        # -------------------------------
        # Calculate the negative noise ratio (fewer noise points is better).
        # -------------------------------
        neg_noise = -((labels == -1).sum() / len(labels))
        self.logger.debug("Computed metrics: silhouette=%.4f, neg_noise=%.4f", silhouette, neg_noise)
        return {"silhouette": silhouette, "neg_noise": neg_noise}

    def _triple_objective(self, trial, embeddings):
        """
        Objective function for Optuna optimization combining three metrics.

        This function applies UMAP and HDBSCAN with hyperparameters from the trial, computes clustering metrics,
        and returns a triple of objectives:
            - Silhouette score (to maximize).
            - Negative noise ratio (to maximize, which corresponds to minimizing the noise ratio).
            - Negative number of clusters (to maximize, i.e. favor fewer clusters).

        If any errors occur or constraints are not met (e.g., noise ratio or cluster count outside allowed range),
        the function returns a triple of -infinity values to indicate an invalid trial.

        Args:
            trial (optuna.trial.Trial): Optuna trial for hyperparameter suggestions.
            embeddings (np.ndarray): Array of embedding vectors.

        Returns:
            list: A list containing [silhouette, negative noise ratio, negative number of clusters].
        """
        self.logger.debug("Starting triple-objective evaluation for trial number: %s", trial.number if hasattr(trial, 'number') else 'N/A')
        try:
            # -------------------------------
            # Create models using trial-specific hyperparameters.
            # -------------------------------
            umap_model, hdbscan_model, _, _ = self._create_models(trial, len(embeddings))
            self.logger.debug("Models created for trial %s", trial.number if hasattr(trial, 'number') else 'N/A')
            
            # -------------------------------
            # Apply UMAP dimensionality reduction.
            # -------------------------------
            reduced_data = umap_model.fit_transform(X=embeddings)
            self.logger.debug("UMAP reduction completed for trial %s", trial.number if hasattr(trial, 'number') else 'N/A')
            
            # -------------------------------
            # Run HDBSCAN clustering.
            # -------------------------------
            hdbscan_model.fit(reduced_data)
            # -------------------------------
            # If branch detection is enabled, run BranchDetector with trial-sampled hyperparameters.
            # -------------------------------
            if self.hdbscan_branch_detection:
                branch_params = self._create_branch_params(trial)
                from hdbscan import BranchDetector
                branch_detector = BranchDetector(
                    min_branch_size=branch_params["min_branch_size"],
                    allow_single_branch=False,
                    branch_detection_method="full",  # fixed as per instructions
                    branch_selection_method="eom",     # fixed as per instructions
                    branch_selection_persistence=branch_params["branch_selection_persistence"],
                    label_sides_as_branches=branch_params["label_sides_as_branches"]
                )
                labels = branch_detector.fit_predict(X=hdbscan_model) # type: ignore
                
            else:
                labels = hdbscan_model.labels_
                
            
            self.logger.debug("Clustering produced labels: %s", labels)
            
            # -------------------------------
            # Compute clustering metrics (silhouette and negative noise ratio).
            # -------------------------------
            metrics_result = self._compute_metrics(reduced_data=reduced_data, labels=labels)
            if metrics_result is None:
                self.logger.debug("Metrics result invalid for trial %s; returning -inf objectives.", trial.number if hasattr(trial, 'number') else 'N/A')
                return [float("-inf")] * 3

            # -------------------------------
            # Extract metrics and compute noise ratio (invert negative noise ratio).
            # -------------------------------
            s = metrics_result["silhouette"]
            neg_noise = metrics_result["neg_noise"]
            noise_ratio = -neg_noise  # actual noise ratio

            # -------------------------------
            # Enforce noise ratio constraints.
            # -------------------------------
            if noise_ratio < self.min_noise_ratio or noise_ratio > self.max_noise_ratio:
                self.logger.debug("Trial %s failed noise ratio constraints (noise_ratio=%.4f).", trial.number if hasattr(trial, 'number') else 'N/A', noise_ratio)
                return [float("-inf")] * 3
            
            # -------------------------------
            # Compute number of clusters (excluding noise).
            # -------------------------------
            k = len(set(labels) - {-1})
            self.logger.debug("Trial %s metrics: silhouette=%.4f, neg_noise=%.4f, clusters=%d", trial.number if hasattr(trial, 'number') else 'N/A', s, neg_noise, k)
            
            # -------------------------------
            # Enforce cluster count constraints.
            # -------------------------------
            if k < self.min_clusters or k > self.max_clusters:
                self.logger.debug("Trial %s failed cluster count constraints (k=%d).", trial.number if hasattr(trial, 'number') else 'N/A', k)
                return [float("-inf")] * 3
            
            neg_k = -k  # Fewer clusters is better.
            return [s, neg_noise, neg_k]
        except Exception as e:
            # -------------------------------
            # Log any error that occurs and mark this trial as invalid.
            # -------------------------------
            self.logger.error("Trial failed with error: %s", str(e))
            return [float("-inf")] * 3

    def _euclidean_distance_3d(self, x1, y1, z1, x2, y2, z2) -> float:
        """
        Compute the Euclidean distance between two points in 3D space.

        Args:
            x1, y1, z1 (float): Coordinates of the first point.
            x2, y2, z2 (float): Coordinates of the second point.

        Returns:
            float: The Euclidean distance between the two points.
        """
        # -------------------------------
        # Calculate the Euclidean distance using the standard 3D distance formula.
        # -------------------------------
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        self.logger.debug("Computed Euclidean distance between (%.4f, %.4f, %.4f) and (%.4f, %.4f, %.4f): %.4f", x1, y1, z1, x2, y2, z2, distance)
        return distance

    def _get_best_solution(self, study, pareto_trials):
        """
        Select the best trial from the Pareto optimal solutions using the TOPSIS method.

        The Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is applied on the Pareto front.
        Each trial's metrics (silhouette, negative noise, and negative number of clusters) are normalized,
        and distances to the ideal and anti-ideal solutions are computed. The trial with the highest TOPSIS
        score is selected.

        Args:
            study (optuna.study.Study): The Optuna study containing all trials.
            pareto_trials (list): List of Pareto-optimal trials with valid metric values.

        Returns:
            tuple: A tuple containing:
                - best_trial (optuna.trial.FrozenTrial): The selected best trial.
                - str: A string indicating the selection method ("pareto_topsis").

        Raises:
            ValueError: If no valid Pareto optimal solutions are found.
        """
        self.logger.info("Selecting best solution from %d Pareto trials.", len(pareto_trials))
        if pareto_trials:
            try:
                # -------------------------------
                # Extract and collect metrics from each Pareto trial.
                # -------------------------------
                trial_details = []
                for t in pareto_trials:
                    trial_details.append({
                        "trial": t,
                        "silhouette": t.values[0],
                        "neg_noise": t.values[1],
                        "neg_k": t.values[2],
                    })
                self.logger.info("Extracted trial details: %s", trial_details)
                
                # -------------------------------
                # Collect lists of each individual metric for normalization.
                # -------------------------------
                sil_vals = [d["silhouette"] for d in trial_details]
                noise_vals = [d["neg_noise"] for d in trial_details]
                k_vals = [d["neg_k"] for d in trial_details]

                # -------------------------------
                # Define a normalization function (Euclidean norm factor).
                # -------------------------------
                def norm_factor(vals) -> float:
                    return math.sqrt(sum(v * v for v in vals))

                # -------------------------------
                # Calculate normalization factors for each metric.
                # -------------------------------
                sil_norm: float = norm_factor(vals=sil_vals)
                noise_norm: float = norm_factor(vals=noise_vals)
                k_norm: float = norm_factor(vals=k_vals)
                self.logger.info("Normalization factors: sil_norm=%.4f, noise_norm=%.4f, k_norm=%.4f", sil_norm, noise_norm, k_norm)

                # -------------------------------
                # Normalize each trial's metrics.
                # -------------------------------
                normalized = []
                for d in trial_details:
                    s_norm = d["silhouette"] / sil_norm if sil_norm != 0 else 0
                    n_norm = d["neg_noise"] / noise_norm if noise_norm != 0 else 0
                    k_norm_val = d["neg_k"] / k_norm if k_norm != 0 else 0
                    normalized.append({**d, "s_norm": s_norm, "n_norm": n_norm, "k_norm": k_norm_val})
                self.logger.info("Normalized trial metrics: %s", normalized)

                # -------------------------------
                # Determine ideal (max) and anti-ideal (min) normalized values for each metric.
                # -------------------------------
                s_norm_vals = [item["s_norm"] for item in normalized]
                n_norm_vals = [item["n_norm"] for item in normalized]
                k_norm_vals = [item["k_norm"] for item in normalized]

                ideal_s = max(s_norm_vals)
                ideal_n = max(n_norm_vals)
                ideal_k = max(k_norm_vals)

                anti_s = min(s_norm_vals)
                anti_n = min(n_norm_vals)
                anti_k = min(k_norm_vals)
                self.logger.info(
                    "Ideal values: (%.4f, %.4f, %.4f), Anti-ideal values: (%.4f, %.4f, %.4f)",
                    ideal_s, 
                    ideal_n, 
                    ideal_k, 
                    anti_s, 
                    anti_n, 
                    anti_k
                )

                # -------------------------------
                # Compute TOPSIS score for each trial by comparing distances to ideal and anti-ideal points.
                # -------------------------------
                topsised = []
                for item in normalized:
                    dist_ideal: float = self._euclidean_distance_3d(
                        x1=item["s_norm"], 
                        y1=item["n_norm"], 
                        z1=item["k_norm"],
                        x2=ideal_s, 
                        y2=ideal_n, 
                        z2=ideal_k
                    )
                    dist_anti = self._euclidean_distance_3d(
                        x1=item["s_norm"], 
                        y1=item["n_norm"], 
                        z1=item["k_norm"],
                        x2=anti_s, 
                        y2=anti_n, 
                        z2=anti_k
                    )
                    # Compute TOPSIS score (ratio of distance to anti-ideal over total distance).
                    topsis_score = dist_anti / (dist_ideal + dist_anti) if (dist_ideal + dist_anti) != 0 else 0
                    topsised.append({**item, "dist_ideal": dist_ideal, "dist_anti": dist_anti, "score": topsis_score})
                
                # -------------------------------
                # Log the TOPSIS scores for all Pareto trials.
                # -------------------------------
                self.logger.info("\n*** TOPSIS on Pareto front ***")
                for i, item in enumerate(sorted(topsised, key=lambda x: -x["score"]), 1):
                    self.logger.info("%d) Trial #%d - Score: %.4f", i, item['trial'].number, item['score'])
                    self.logger.info("    Silhouette: %.4f", item['silhouette'])
                    self.logger.info("    -Noise:     %.4f", item['neg_noise'])
                    self.logger.info("    -k:         %.4f", item['neg_k'])
                
                # -------------------------------
                # Select the trial with the highest TOPSIS score.
                # -------------------------------
                best_sol = max(topsised, key=lambda x: x["score"])
                best_trial = best_sol["trial"]
                self.logger.info("\nSelected by TOPSIS => Trial #%d with Score = %.4f", best_trial.number, best_sol['score'])
                self.logger.debug("Best trial selected: %s", best_trial)
                return best_trial, "pareto_topsis"
            except Exception as e:
                self.logger.error("TOPSIS failed with error: %s", str(e))
        # -------------------------------
        # If no valid Pareto solutions found, log error and raise an exception.
        # -------------------------------
        self.logger.error("No valid Pareto optimal solutions found... Raising error.")
        raise ValueError(
            "No valid solutions found during hyperparameter optimization. Try again with more data."
        )

    def _interpret_metric(self, metric_name, value):
        """
        Automatically interpret clustering metrics based on predefined ranges.

        Args:
            metric_name (str): The name of the metric to interpret.
            value (float or int): The value of the metric.

        Returns:
            str: Interpretation message for the metric.
        """
        match metric_name:
            case "n_clusters":
                match value:
                    case v if self.min_clusters <= v <= self.min_clusters * (1 + 0.15):
                        return "a bit low. Consider re-running if silhouette score is low and/or noise is high."
                    case v if self.max_clusters * (1 - 0.15) <= v <= self.max_clusters:
                        return "kinda high. Consider re-running if silhouette score is high and/or noise is low."
                    case _:
                        return "OK."
                    
            case "noise_ratio":
                match value:
                    case v if v < self.min_noise_ratio:
                        return "too good to be true. Consider re-running, especially if number of clusters is high and/or silhouette score is low."
                    case v if self.min_noise_ratio <= v <= self.max_noise_ratio:
                        return "OK."
                    case _:
                        return "too high. Consider re-running, especially if number of clusters is low and/or avg silhouette score is high."
                    
            case "silhouette_score":
                match value:
                    case v if 0.47 <= v < 0.77:
                        return "good."
                    case v if 0.35 <= v < 0.47:
                        return "so-so. Could be better. Consider re-running."
                    case v if v < 0.35:
                        return "poor. Consider re-running, especially if number of clusters is low and/or noise is low."
                    case _:
                        return "too good to be true. Consider re-running, especially if number of clusters is high."
            case _:
                return "unknown metric"

    def _pca_preprocess(self, df: pd.DataFrame):
        """
        Preprocess the DataFrame using PCA to reduce the dimensionality of the embedding vectors.
        This method uses a binary search to find the smallest number of PCA components such that
        the cumulative explained variance ratio is at least the threshold defined by self.target_pca_evr.
        The original embedding column (specified by self.embedding_col_name) is then replaced with the PCA-reduced vectors.

        Args:
            df (pd.DataFrame): A copy of the original DataFrame containing the embedding vectors.

        Returns:
            dict: A dictionary containing:
                - 'df': The DataFrame with the embedding column replaced by PCA-reduced vectors.
                - 'pca_model': The fitted PCA model.
        """
        self.logger.info("Starting PCA preprocessing with binary search to achieve an explained variance ratio >= %.2f", self.target_pca_evr)
        # Convert embedding vectors to a 2D numpy array.
        X = np.vstack(df[self.embedding_col_name].values)  # type: ignore
        orig_dim = X.shape[1]
        self.logger.debug("Original embeddings shape: %s", X.shape)

        # Set the search bounds for the number of components.
        low = 1
        high = orig_dim
        best_n_components = high  # Initialize with the maximum possible value.

        # Binary search for the minimal number of components satisfying the EVR threshold.
        while low <= high:
            mid = (low + high) // 2
            pca = PCA(n_components=mid, random_state=self.random_state, svd_solver='randomized')
            pca.fit(X)
            evr = float(np.sum(pca.explained_variance_ratio_))
            self.logger.debug("Binary search trial: n_components=%d, EVR=%.4f", mid, evr)

            if evr >= self.target_pca_evr: #type: ignore
                # Found a candidate, try to see if a lower number of components works.
                best_n_components = mid
                high = mid - 1
            else:
                # Increase the number of components.
                low = mid + 1

        # Re-fit PCA with the best number of components found.
        pca_model = PCA(n_components=best_n_components, random_state=self.random_state, svd_solver='randomized')
        X_reduced = pca_model.fit_transform(X)
        self.logger.info("PCA preprocessing complete: selected n_components=%d with EVR=%.4f", best_n_components, float(np.sum(pca_model.explained_variance_ratio_)))
        # Replace the embedding column in the DataFrame with the PCA-reduced vectors.
        df[self.embedding_col_name] = [list(row) for row in X_reduced]
        return {"pcd_reduced_df": df, "pca_model": pca_model}

    def optimize(self, filtered_df: pd.DataFrame):
        """
        Optimize UMAP and HDBSCAN hyperparameters and perform clustering on the input DataFrame.

        This method takes a DataFrame containing an embedding vector column (specified by self.embedding_col_name),
        first applies PCA preprocessing to reduce the dimensionality of the embeddings (ensuring that the cumulative
        explained variance ratio is at least self.target_pca_evr), then performs hyperparameter tuning using a triple-objective
        optimization (silhouette score, negative noise ratio, and negative cluster count), and selects the best model using TOPSIS
        on the Pareto front. If no valid Pareto-optimal trial is found, the method falls back to default hyperparameters computed as the average of
        the provided min/max values.

        The final DataFrame is augmented with:
            - A 'reduced_vector' column containing the reduced-dimension coordinates as a list for each entry.
            - Cluster labels in 'cluster_id'.
            - Membership strengths, outlier scores, and a 'core_point' boolean column.

        Args:
            filtered_df (pd.DataFrame): Input DataFrame with an embedding column specified by self.embedding_col_name.

        Returns:
            dict: A dictionary containing:
                - 'clustered_df': The DataFrame with added columns 'membership_strength', 'core_point', 'outlier_score', 'reduced_vector', and 'cluster_id'.
                - 'umap_model': The final UMAP model instance.
                - 'hdbscan_model': The final HDBSCAN model instance.
                - 'pca_model': The fitted PCA model used for preprocessing.
                - 'metrics_dict': Dictionary of key metrics including reduced dimensions, number of clusters, noise ratio, and silhouette score (if computed).
                - 'branch_detector': The fitted BranchDetector if branch detection is enabled, else None.
        """
        branch_detector_final = None  # Will hold the fitted BranchDetector if used.
        try:
            self.logger.debug("Starting optimization process on DataFrame with %d rows", len(filtered_df))
            # -------------------------------
            # Validate input: Check if the DataFrame contains the required embedding column.
            # -------------------------------
            if self.embedding_col_name not in filtered_df.columns:
                self.logger.error(f"Input DataFrame must contain a(n) {self.embedding_col_name} column.")
                raise ValueError(f"Missing {self.embedding_col_name} column in input DataFrame.")

            # -------------------------------
            # PCA Preprocessing: Optimize PCA to reduce dimensionality while retaining sufficient variance.
            # -------------------------------
            if self.target_pca_evr is not None:
                pca_result = self._pca_preprocess(filtered_df.copy())
                filtered_df = pca_result["pcd_reduced_df"]
                pca_model = pca_result["pca_model"]
                self.logger.debug("PCA preprocessing complete. Updated DataFrame with PCA-reduced embeddings.")
            else:
                pca_model = None
                self.logger.debug("target_pca_evr was set to None. Skipping PCA preprocessing step. Using the original full-dimensional embeddings instead.")

            # -------------------------------
            # Convert embedding vectors to a 2D numpy array.
            # -------------------------------
            embeddings = np.vstack(filtered_df[self.embedding_col_name].values)  # type: ignore
            num_data_pts = len(filtered_df)
            self.logger.debug("Converted embedding vectors to numpy array with shape: %s", embeddings.shape)

            self.logger.info("Starting triple-objective optimization (silhouette, -noise, -k).")
            # -------------------------------
            # Create an Optuna study configured for multi-objective optimization.
            # -------------------------------
            study = optuna.create_study(
                directions=["maximize", "maximize", "maximize"],
                sampler=optuna.samplers.NSGAIISampler(seed=self.random_state),
            )
            self.logger.debug("Optuna study created with directions maximize for all objectives.")
            
            # -------------------------------
            # Run the hyperparameter optimization for a specified number of trials.
            # -------------------------------
            study.optimize(
                lambda trial: self._triple_objective(trial=trial, embeddings=embeddings),
                n_trials=self.n_trials,
                n_jobs=self.optuna_jobs,
                show_progress_bar=True,
            )
            self.logger.debug("Optuna optimization completed.")

            # -------------------------------
            # Extract Pareto-optimal trials with valid metric values.
            # -------------------------------
            pareto_trials = [t for t in study.best_trials if not any(math.isinf(x) for x in t.values)]
            self.logger.info("\nPareto front trials:")
            self.logger.info("Number of Pareto-optimal solutions: %d", len(pareto_trials))
            # -------------------------------
            # Log details for each Pareto trial.
            # -------------------------------
            for i, trial in enumerate(pareto_trials, 1):
                s_val, neg_noise_val, neg_k_val = trial.values
                self.logger.info("\nSolution %d:", i)
                self.logger.info("    - clusters: %d", int(-neg_k_val))
                self.logger.info("    - silhouette: %.3f", s_val)
                self.logger.info("    - noise ratio: %.3f", -neg_noise_val)
                self.logger.debug("Trial #%d details: values=%s, params=%s", trial.number, trial.values, trial.params)

            # -------------------------------
            # Select the best trial using TOPSIS or fallback to default hyperparameters if no valid trial is found.
            # -------------------------------
            if not pareto_trials:
                self.logger.warning("No valid Pareto-optimal solutions found; falling back to average of min/max hyperparameters.")
                best_umap, best_hdbscan, umap_params, hdbscan_params = self._default_models(num_data_pts)
                dims_final = umap_params["n_components"]
            else:
                # -------------------------------
                # Use TOPSIS to select the best trial from the Pareto front.
                # -------------------------------
                best_trial, method_used = self._get_best_solution(study=study, pareto_trials=pareto_trials)
                self.logger.info("Solution selection method: %s", method_used)
                s_val, neg_noise_val, neg_k_val = best_trial.values
                self.logger.info("\n*** Final Chosen Trial ***")
                self.logger.info(" - Silhouette: %.4f", s_val)
                self.logger.info(" - Neg noise:  %.4f", neg_noise_val)
                self.logger.info(" - Neg k:      %.4f", neg_k_val)
                self.logger.debug("Best trial parameters: %s", best_trial.params)
                dims_final = self.dims if self.dims is not None else best_trial.params["umap_n_components"]

                best_umap, best_hdbscan, umap_params, hdbscan_params = self._create_models(best_trial, num_data_pts)
            
            self.logger.debug("Using final UMAP dims=%d", dims_final)
            # -------------------------------
            # Fit UMAP on embeddings to obtain reduced dimension coordinates.
            # -------------------------------
            reduced_coords = best_umap.fit_transform(embeddings)
            self.logger.debug("UMAP reduction complete. Reduced coordinates shape: %s", reduced_coords.shape)  # type: ignore
            
            # -------------------------------
            # Predict clusters using the final HDBSCAN (and BranchDetector if enabled).
            # -------------------------------
            if self.hdbscan_branch_detection:
                best_hdbscan.fit(reduced_coords)
                from hdbscan import BranchDetector
                # Create a BranchDetector using the best trial's parameters.
                branch_detector_final = BranchDetector(
                    min_branch_size=best_trial.params["branch_min_cluster_size"],
                    allow_single_branch=False,
                    branch_detection_method="full",  # fixed
                    branch_selection_method="eom",     # fixed
                    branch_selection_persistence=best_trial.params["branch_selection_persistence"],
                    label_sides_as_branches=best_trial.params["branch_label_sides_as_branches"]
                )
                final_labels = branch_detector_final.fit_predict(best_hdbscan) # type: ignore
                membership = branch_detector_final.probabilities_
                # Compute core point flags using branch detector probabilities.
                # Since membership score is in the opposite direction of outlier score,
                # we use (100 - hdbscan_outlier_threshold)/100 as the threshold.
                core_threshold = (100 - self.hdbscan_outlier_threshold) / 100.0
                core_flags = membership >= core_threshold
                # Optionally, we do not have a direct outlier score here.
                outlier_scores_final = np.full(len(final_labels), np.nan)
                self.logger.debug("BranchDetector produced branch labels: %s", final_labels)
            else:
                final_labels = best_hdbscan.fit_predict(reduced_coords)  # type: ignore
                membership = best_hdbscan.probabilities_
                outlier_scores_final = best_hdbscan.outlier_scores_
                threshold_val = np.percentile(outlier_scores_final, self.hdbscan_outlier_threshold)
                core_flags = outlier_scores_final < threshold_val

            # -------------------------------
            # Validate that the length of membership probabilities matches the DataFrame.
            # -------------------------------
            if len(membership) != len(filtered_df):
                raise AssertionError(
                    f"Mismatch between probabilities ({len(membership)}) and dataframe length ({len(filtered_df)})"
                )
            # -------------------------------
            # Append clustering metadata (membership strengths, core point, outlier scores) to the DataFrame.
            # -------------------------------
            filtered_df["membership_strength"] = membership
            filtered_df["core_point"] = core_flags
            filtered_df["outlier_score"] = outlier_scores_final
            self.logger.debug("Appended membership_strength, core_point, and outlier_score to DataFrame.")

            # -------------------------------
            # Compute overall clustering metrics (noise ratio, number of clusters, silhouette score).
            # -------------------------------
            noise_ratio = (final_labels == -1).sum() / len(final_labels)
            n_clusters = len(set(final_labels)) - (1 if -1 in final_labels else 0)

            best_sil_score = None
            mask = final_labels != -1
            if np.sum(mask) >= 2:
                best_sil_score = silhouette_score(
                    X=reduced_coords[mask],  # type: ignore
                    labels=final_labels[mask],
                    metric="euclidean",
                )
                self.logger.debug("Computed silhouette score for non-noise points: %.4f", best_sil_score)

            # -------------------------------
            # Log final clustering results and cluster sizes.
            # -------------------------------
            self.logger.info("\n*** Final Clustering Results ***:")
            self.logger.info("Dimensionality: %d", dims_final)
            self.logger.info("Number of clusters: %d", n_clusters)
            if best_sil_score is not None:
                self.logger.info("Silhouette score: %.3f", best_sil_score)
            self.logger.info("Noise ratio: %.1f%%", noise_ratio * 100)

            unique_labels = sorted(set(final_labels))
            if -1 in unique_labels:
                unique_labels.remove(-1)
            self.logger.info("\nCluster sizes:")
            for label in unique_labels:
                size = (final_labels == label).sum()
                self.logger.info("  Cluster %d: %d points (%.1f%%)", label, size, size / len(final_labels) * 100)
                self.logger.debug("Cluster %d size: %d", label, size)

            # -------------------------------
            # Add the reduced dimension vector as a single column in the DataFrame.
            # -------------------------------
            filtered_df["reduced_vector"] = [list(row) for row in reduced_coords]
            self.logger.debug("Added column 'reduced_vector' with reduced dimension vectors.")
            filtered_df["cluster_id"] = final_labels

            # -------------------------------
            # Build a dictionary containing key clustering metrics.
            # -------------------------------
            metrics_dict = {
                "reduced_dimensions": dims_final,
                "n_clusters": n_clusters,
                "noise_ratio": round(float(noise_ratio), 2),
            }
            if best_sil_score is not None:
                metrics_dict["silhouette_score"] = round(float(best_sil_score), 2)
            self.logger.debug("Built metrics_dict: %s", metrics_dict)
            
            #------------------------
            # Interpret the metrics for the user
            #------------------------
            n_clusters_result = self._interpret_metric("n_clusters", metrics_dict["n_clusters"])
            noise_ratio_result = self._interpret_metric("noise_ratio", metrics_dict["noise_ratio"])
            silhouette_result = self._interpret_metric("silhouette_score", metrics_dict.get("silhouette_score", 0))

            self.logger.info(f"""
            
            *** Metrics Interpretation *** 
            (take these with a grain of salt)
            ----------------------------------------------------------------
            The run resulted in {metrics_dict['n_clusters']} clusters, which is {n_clusters_result}
            The run's noise_ratio of {metrics_dict['noise_ratio']} is {noise_ratio_result}
            The run's silhouette_score of {metrics_dict.get('silhouette_score', 'N/A')} is {silhouette_result}
            
            """)
            

            # -------------------------------
            # Finalize and return the clustering results and models.
            # -------------------------------
            self.logger.debug("Optimization process complete. Returning final results.")
            return {
                "clustered_df": filtered_df,
                "umap_model": best_umap,
                "hdbscan_model": best_hdbscan,
                "pca_model": pca_model,
                "metrics_dict": metrics_dict,
                "branch_detector": branch_detector_final,
            }
        except Exception as e:
            self.logger.error("An error occurred during clustering optimization: %s", str(e))
            raise

def run_clustering(
    filtered_df: pd.DataFrame,
    dims=3, 
    min_clusters=3,
    max_clusters=25,
    n_trials=20, 
    random_state=42,
    embedding_col_name="embedding_vector",
    
    umap_n_neighbors_min=2,
    umap_n_neighbors_max=25,
    umap_min_dist_min=0.0,
    umap_min_dist_max=0.1,
    umap_spread_min=1.0,
    umap_spread_max=10.0,
    umap_learning_rate_min=0.08,
    umap_learning_rate_max=1.0,
    umap_min_dims=2,
    umap_max_dims=20,
    umap_metric="cosine",
    
    hdbscan_min_cluster_size_multiplier_min=0.005,
    hdbscan_min_cluster_size_multiplier_max=0.025,
    hdbscan_min_samples_min=2,
    hdbscan_min_samples_max=50,
    hdbscan_epsilon_min=0.0,
    hdbscan_epsilon_max=1.0,
    hdbscan_metric="euclidean",
    hdbscan_cluster_selection_method="eom",
    
    optuna_jobs=-1,
    hdbscan_outlier_threshold=90,
    min_noise_ratio=0.03,
    max_noise_ratio=0.35,

    target_pca_evr=0.9,
    
    hdbscan_branch_detection=False
):
    """
    Perform clustering on a DataFrame containing embedding vectors.

    This function is a convenient functional interface for using the ClusteringEngine.
    It expects the DataFrame to have an embedding column defined by the parameter 'embedding_col_name'
    and returns a dictionary with:
        - 'clustered_df': The DataFrame augmented with clustering results (additional columns: 'membership_strength', 'core_point', 'outlier_score', 'reduced_vector', and 'cluster_id').
        - 'umap_model': The UMAP model instance used for dimensionality reduction.
        - 'hdbscan_model': The HDBSCAN model instance used for clustering.
        - 'pca_model': The PCA model instance used for preprocessing.
        - 'metrics_dict': A dictionary containing key clustering metrics.
        - 'branch_detector': The fitted BranchDetector if branch detection is enabled, else None.

    Args:
        filtered_df (pd.DataFrame): DataFrame containing the embedding vectors in the column specified by embedding_col_name.
        dims (int or None): Number of dimensions for UMAP reduction.
        min_clusters (int): Minimum acceptable number of clusters.
        max_clusters (int): Maximum acceptable number of clusters.
        n_trials (int): Number of optimization trials for hyperparameter tuning.
        random_state: Seed for reproducibility.
        embedding_col_name (str): Name of the column containing embedding vectors.
        umap_n_neighbors_min (int): Minimum value for UMAP's n_neighbors parameter.
        umap_n_neighbors_max (int): Maximum value for UMAP's n_neighbors parameter.
        umap_min_dist_min (float): Minimum value for UMAP's min_dist parameter.
        umap_min_dist_max (float): Maximum value for UMAP's min_dist parameter.
        umap_spread_min (float): Minimum value for UMAP's spread parameter.
        umap_spread_max (float): Maximum value for UMAP's spread parameter.
        umap_learning_rate_min (float): Minimum value for UMAP's learning_rate parameter.
        umap_learning_rate_max (float): Maximum value for UMAP's learning_rate parameter.
        umap_min_dims (int): Minimum number of dimensions for UMAP reduction.
        umap_max_dims (int): Maximum number of dimensions for UMAP reduction.
        umap_metric (str): Distance metric to use for UMAP.
        hdbscan_min_cluster_size_multiplier_min (float): Minimum multiplier for HDBSCAN's min_cluster_size.
        hdbscan_min_cluster_size_multiplier_max (float): Maximum multiplier for HDBSCAN's min_cluster_size.
        hdbscan_min_samples_min (int): Minimum value for HDBSCAN's min_samples parameter.
        hdbscan_min_samples_max (int): Maximum value for HDBSCAN's min_samples parameter.
        hdbscan_epsilon_min (float): Minimum value for HDBSCAN's cluster_selection_epsilon parameter.
        hdbscan_epsilon_max (float): Maximum value for HDBSCAN's cluster_selection_epsilon parameter.
        hdbscan_metric (str): Distance metric to use for HDBSCAN clustering.
        hdbscan_cluster_selection_method (str): Method to use for selecting clusters in HDBSCAN.
        optuna_jobs (int): Number of parallel jobs to run during Optuna optimization.
        hdbscan_outlier_threshold (int): Percentile threshold for HDBSCAN outlier detection.
        min_noise_ratio (float): Minimum acceptable noise ratio.
        max_noise_ratio (float): Maximum acceptable noise ratio.
        target_pca_evr (float): Minimum explained variance ratio for PCA preprocessing.
        hdbscan_branch_detection (bool): Whether to enable branch detection in HDBSCAN. Useful if your silhoutte plot shows "fat" rounded clusters.

    Returns:
        dict: Dictionary containing:
            - 'clustered_df': The DataFrame with clustering results.
            - 'umap_model': The UMAP model instance used.
            - 'hdbscan_model': The HDBSCAN model instance used.
            - 'pca_model': The PCA model instance used.
            - 'metrics_dict': Key clustering metrics.
            - 'branch_detector': The fitted BranchDetector if branch detection is enabled, else None.
    """
    try:
        logging.debug("cluster() function called.")
        # -------------------------------
        # Create an instance of ClusteringEngine and start the optimization process.
        # -------------------------------
        clustering = ClusteringEngine(
            dims=dims,
            min_clusters=min_clusters,
            max_clusters=max_clusters,
            n_trials=n_trials,
            random_state=random_state,
            embedding_col_name=embedding_col_name,
            umap_n_neighbors_min=umap_n_neighbors_min,
            umap_n_neighbors_max=umap_n_neighbors_max,
            umap_min_dist_min=umap_min_dist_min,
            umap_min_dist_max=umap_min_dist_max,
            umap_spread_min=umap_spread_min,
            umap_spread_max=umap_spread_max,
            umap_learning_rate_min=umap_learning_rate_min,
            umap_learning_rate_max=umap_learning_rate_max,
            umap_min_dims=umap_min_dims,
            umap_max_dims=umap_max_dims,
            umap_metric=umap_metric,
            hdbscan_min_cluster_size_multiplier_min=hdbscan_min_cluster_size_multiplier_min,
            hdbscan_min_cluster_size_multiplier_max=hdbscan_min_cluster_size_multiplier_max,
            hdbscan_min_samples_min=hdbscan_min_samples_min,
            hdbscan_min_samples_max=hdbscan_min_samples_max,
            hdbscan_epsilon_min=hdbscan_epsilon_min,
            hdbscan_epsilon_max=hdbscan_epsilon_max,
            hdbscan_metric=hdbscan_metric,
            hdbscan_cluster_selection_method=hdbscan_cluster_selection_method,
            optuna_jobs=optuna_jobs,
            hdbscan_outlier_threshold=hdbscan_outlier_threshold,
            min_noise_ratio=min_noise_ratio,
            max_noise_ratio=max_noise_ratio,
            target_pca_evr=target_pca_evr,
            hdbscan_branch_detection=hdbscan_branch_detection,
        )
        logging.debug("ClusteringEngine instance created. Calling optimize().")
        result = clustering.optimize(filtered_df=filtered_df.copy())
        logging.debug("Clustering process completed successfully.")
        return result
    except Exception as e:
        logging.error("An error occurred in the clustering process: %s", str(e))
        raise
