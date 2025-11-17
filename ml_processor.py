import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
import warnings
warnings.filterwarnings('ignore')

def process_clustering(filepath):
    """
    Process CSV file and perform KMeans clustering.
    Returns clustering results including cluster assignments and metrics.
    """
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Check if required columns exist
    required_cols = ["gaming_platform_top1", "social_platform_top1", "ott_top1", 
                     "content_creation_freq", "daily_social_media_minutes"]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check for name column (if exists, use it; otherwise use index)
    if 'name' in df.columns:
        name_col = 'name'
    elif 'Name' in df.columns:
        name_col = 'Name'
    elif 'person_name' in df.columns:
        name_col = 'person_name'
    else:
        # Create a name column from index if no name column exists
        df['name'] = df.index.astype(str)
        name_col = 'name'
    
    # Store original dataframe for results
    df_original = df.copy()
    
    # Encode categorical columns
    cat_cols = ["gaming_platform_top1", "social_platform_top1", "ott_top1", "content_creation_freq"]
    encoders = {col: LabelEncoder().fit(df[col]) for col in cat_cols}
    
    for col in cat_cols:
        df[col] = encoders[col].transform(df[col])
    
    # Scale numerical features
    scaler = StandardScaler()
    X = df[cat_cols + ["daily_social_media_minutes"]].copy()
    X["daily_social_media_minutes"] = scaler.fit_transform(
        X[["daily_social_media_minutes"]]
    )
    
    X = X.to_numpy()
    
    # Find optimal k using elbow method
    ks = []
    inertias = []
    
    max_k = min(15, len(df) // 2)  # Don't exceed reasonable k values
    for k in range(1, max_k + 1):
        if k >= len(df):
            break
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        ks.append(k)
        inertias.append(kmeans.inertia_)
    
    # Simple elbow detection (find the point with maximum curvature)
    if len(inertias) > 2:
        # Calculate rate of change
        diffs = np.diff(inertias)
        second_diffs = np.diff(diffs)
        if len(second_diffs) > 0:
            k_opt = ks[np.argmax(second_diffs) + 1]
        else:
            k_opt = 2
    else:
        k_opt = 2
    
    # Ensure k_opt is at least 2 and reasonable
    k_opt = max(2, min(k_opt, len(df) // 2))
    
    # Perform clustering with optimal k
    kmeans_model = KMeans(n_clusters=k_opt, random_state=42, n_init=10)
    kmeans_model.fit(X)
    
    # Add cluster labels to dataframe
    df_original["Cluster"] = kmeans_model.labels_
    
    # Calculate metrics
    sil_score = silhouette_score(X, kmeans_model.labels_)
    db_index = davies_bouldin_score(X, kmeans_model.labels_)
    
    # Prepare results: group by cluster and get person names
    clusters_data = {}
    for cluster_id in range(k_opt):
        cluster_df = df_original[df_original["Cluster"] == cluster_id]
        names = cluster_df[name_col].tolist()
        clusters_data[f"Cluster {cluster_id}"] = names
    
    # Prepare PCA data for visualization (optional)
    try:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        pca_data = {
            'x': X_pca[:, 0].tolist(),
            'y': X_pca[:, 1].tolist(),
            'clusters': kmeans_model.labels_.tolist()
        }
    except:
        pca_data = None
    
    # Return results
    result = {
        'num_clusters': k_opt,
        'clusters': clusters_data,
        'metrics': {
            'silhouette_score': round(sil_score, 3),
            'davies_bouldin_index': round(db_index, 3)
        },
        'total_persons': len(df_original),
        'pca_data': pca_data,
        'elbow_data': {
            'k_values': ks,
            'inertias': [float(x) for x in inertias]
        }
    }
    
    return result


