import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
import warnings
import re
warnings.filterwarnings('ignore')

def normalize_column_name(col):
    """Normalize column name for matching (lowercase, remove spaces, underscores)"""
    return re.sub(r'[_\s]+', '_', col.lower().strip())

def find_column_by_pattern(df, patterns):
    """
    Find a column in dataframe by matching against multiple patterns.
    Returns the first matching column name or None.
    """
    normalized_cols = {normalize_column_name(col): col for col in df.columns}
    
    for pattern in patterns:
        pattern_norm = normalize_column_name(pattern)
        # Extract key words from pattern (remove common words)
        pattern_words = [w for w in pattern_norm.split('_') if len(w) > 2]
        
        # Exact match
        if pattern_norm in normalized_cols:
            return normalized_cols[pattern_norm]
        
        # Partial match (contains) - check if pattern is in column name
        for norm_col, orig_col in normalized_cols.items():
            if pattern_norm in norm_col or norm_col in pattern_norm:
                return orig_col
        
        # Word-based matching (for long column names with extra text)
        if len(pattern_words) > 0:
            for norm_col, orig_col in normalized_cols.items():
                # Check if all key words from pattern are in the column name
                if all(word in norm_col for word in pattern_words if len(word) > 3):
                    return orig_col
    return None

def detect_columns(df):
    """
    Automatically detect and map columns from various CSV formats.
    Returns a dictionary with detected column names.
    """
    detected = {}
    
    # Name column patterns
    name_patterns = ['name', 'person_name', 'person', 'id', 'user']
    detected['name'] = find_column_by_pattern(df, name_patterns)
    if not detected['name']:
        # Create name column from index
        df['name'] = ['Person_' + str(i+1) for i in range(len(df))]
        detected['name'] = 'name'
    
    # Categorical columns - OTT platform
    ott_patterns = ['ott', 'ott_top1', 'ott_platform', 'streaming_platform', 'platform']
    detected['ott'] = find_column_by_pattern(df, ott_patterns)
    
    # Categorical columns - Genre/Movie/Series
    genre_patterns = ['movie_genre', 'genre', 'movie_genre_top1', 'series_genre', 'series_genre_top1', 
                     'content_genre', 'preferred_genre']
    detected['genre'] = find_column_by_pattern(df, genre_patterns)
    
    # Categorical columns - Language
    lang_patterns = ['content_lang', 'language', 'content_lang_top1', 'preferred_language', 'lang']
    detected['language'] = find_column_by_pattern(df, lang_patterns)
    
    # Categorical columns - Gaming platform (old format)
    gaming_patterns = ['gaming_platform', 'gaming_platform_top1', 'game_platform']
    detected['gaming'] = find_column_by_pattern(df, gaming_patterns)
    
    # Categorical columns - Social platform (old format)
    social_patterns = ['social_platform', 'social_platform_top1', 'social_media_platform']
    detected['social'] = find_column_by_pattern(df, social_patterns)
    
    # Numerical columns - Binge frequency
    binge_patterns = ['binge_frequency', 'binge_freq', 'binge frequency per week', 
                     'content_creation_freq', 'content_creation_frequency']
    detected['binge_freq'] = find_column_by_pattern(df, binge_patterns)
    
    # Numerical columns - Screen time
    screen_patterns = ['screen_time', 'screen time', 'screen_time_hours', 
                      'daily_social_media_minutes', 'social_media_minutes',
                      'Screen Time Movies/series in hours per week',
                      'movies/series', 'hours per week', 'screen']
    detected['screen_time'] = find_column_by_pattern(df, screen_patterns)
    
    # Numerical columns - Gaming days
    gaming_days_patterns = ['gaming_days', 'gaming days per week', 'gaming_frequency', 
                           'gaming_days_per_week']
    detected['gaming_days'] = find_column_by_pattern(df, gaming_days_patterns)
    
    return detected

def process_clustering(filepath):
    """
    Process CSV file and perform KMeans clustering.
    Automatically detects columns from various CSV formats.
    Returns clustering results including cluster assignments and metrics.
    """
    # Read the CSV file - handle various encoding and formatting issues
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except:
            df = pd.read_csv(filepath, encoding='cp1252')
    
    # Clean column names (remove extra spaces, handle multi-line headers, newlines)
    df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('\r', ' ')
    # Remove extra whitespace from column names
    df.columns = df.columns.str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # Remove empty rows and rows where all values are empty strings
    df = df.dropna(how='all')
    df = df[~df.astype(str).apply(lambda x: x.str.strip().eq('') | x.eq('nan')).all(axis=1)]
    
    # Remove rows that look like header continuations (e.g., rows with mostly text in parentheses or instructions)
    # Check if first row after header looks like a continuation (has many empty cells or instruction-like text)
    if len(df) > 0:
        first_row = df.iloc[0].astype(str)
        # If first row has many empty values or looks like instructions, drop it
        empty_count = first_row.str.strip().eq('').sum() + first_row.str.contains('provide|between|value', case=False, na=False).sum()
        if empty_count > len(df.columns) * 0.5:  # More than 50% empty or instruction-like
            df = df.iloc[1:].reset_index(drop=True)
    
    if len(df) == 0:
        raise ValueError("CSV file is empty or contains no valid data")
    
    # Detect columns automatically
    detected_cols = detect_columns(df)
    
    # Store original dataframe for results
    df_original = df.copy()
    name_col = detected_cols['name']
    
    # Prepare features for clustering
    cat_cols = []
    num_cols = []
    
    # Add categorical features (at least 2 needed for meaningful clustering)
    if detected_cols['ott']:
        cat_cols.append(detected_cols['ott'])
    if detected_cols['genre']:
        cat_cols.append(detected_cols['genre'])
    if detected_cols['language']:
        cat_cols.append(detected_cols['language'])
    if detected_cols['gaming']:
        cat_cols.append(detected_cols['gaming'])
    if detected_cols['social']:
        cat_cols.append(detected_cols['social'])
    
    # Add numerical features
    if detected_cols['binge_freq']:
        num_cols.append(detected_cols['binge_freq'])
    if detected_cols['screen_time']:
        num_cols.append(detected_cols['screen_time'])
    if detected_cols['gaming_days']:
        num_cols.append(detected_cols['gaming_days'])
    
    # Validate we have enough features
    if len(cat_cols) + len(num_cols) < 2:
        available_cols = [col for col in df.columns if col != name_col]
        raise ValueError(
            f"Insufficient features detected for clustering. "
            f"Found {len(cat_cols)} categorical and {len(num_cols)} numerical features. "
            f"Available columns: {available_cols}. "
            f"Please ensure your CSV has at least 2 feature columns (categorical or numerical)."
        )
    
    # Create a working copy
    df_work = df.copy()
    
    # Encode categorical columns
    encoders = {}
    for col in cat_cols:
        # Handle missing values
        df_work[col] = df_work[col].fillna('Unknown')
        # Convert to string for encoding
        df_work[col] = df_work[col].astype(str)
        encoders[col] = LabelEncoder()
        df_work[col] = encoders[col].fit_transform(df_work[col])
    
    # Handle numerical columns
    for col in num_cols:
        # Convert to numeric, handling any non-numeric values
        df_work[col] = pd.to_numeric(df_work[col], errors='coerce')
        # Fill missing values with median
        df_work[col] = df_work[col].fillna(df_work[col].median())
    
    # Prepare feature matrix
    feature_cols = cat_cols + num_cols
    X = df_work[feature_cols].copy()
    
    # Scale all features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X = X_scaled
    
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


