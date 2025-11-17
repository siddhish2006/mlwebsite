let selectedFile = null;
let elbowChart = null;
let pcaChart = null;

// File input handling
const fileInput = document.getElementById('fileInput');
const uploadBox = document.getElementById('uploadBox');
const processBtn = document.getElementById('processBtn');

// Upload box click
uploadBox.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'text/csv' || file.name.endsWith('.csv')) {
        handleFileSelect(file);
        fileInput.files = e.dataTransfer.files;
    } else {
        showError('Please upload a CSV file');
    }
});

function handleFileSelect(file) {
    if (file && (file.type === 'text/csv' || file.name.endsWith('.csv'))) {
        selectedFile = file;
        uploadBox.innerHTML = `
            <div class="upload-icon">✅</div>
            <p><strong>${file.name}</strong></p>
            <p class="file-info">File selected. Click "Process Dataset" to continue.</p>
        `;
        processBtn.disabled = false;
        hideError();
    } else {
        showError('Please select a valid CSV file');
    }
}

// Process button click
processBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select a file first');
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    // Show loading
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    hideError();
    processBtn.disabled = true;

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loadingSection').style.display = 'none';
        processBtn.disabled = false;
    }
});

function displayResults(data) {
    // Display metrics
    document.getElementById('numClusters').textContent = data.num_clusters;
    document.getElementById('silhouetteScore').textContent = data.metrics.silhouette_score;
    document.getElementById('dbIndex').textContent = data.metrics.davies_bouldin_index;
    document.getElementById('totalPersons').textContent = data.total_persons;

    // Display clusters
    const clustersContainer = document.getElementById('clustersContainer');
    clustersContainer.innerHTML = '';

    Object.keys(data.clusters).forEach(clusterName => {
        const clusterCard = document.createElement('div');
        clusterCard.className = 'cluster-card';
        
        const persons = data.clusters[clusterName];
        const clusterId = clusterName.replace('Cluster ', '');
        
        // Generate a color for this cluster
        const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140'];
        const color = colors[parseInt(clusterId) % colors.length];
        
        clusterCard.style.borderColor = color;
        
        clusterCard.innerHTML = `
            <div class="cluster-header">
                <span class="cluster-title" style="color: ${color}">${clusterName}</span>
                <span class="cluster-count" style="background: ${color}">${persons.length} persons</span>
            </div>
            <div class="persons-list">
                ${persons.map(person => `<div class="person-item" style="border-left-color: ${color}">${person}</div>`).join('')}
            </div>
        `;
        
        clustersContainer.appendChild(clusterCard);
    });

    // Display elbow chart
    if (data.elbow_data && data.elbow_data.k_values.length > 0) {
        displayElbowChart(data.elbow_data);
    }

    // Display PCA chart
    if (data.pca_data) {
        displayPCAChart(data.pca_data);
    }

    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function displayElbowChart(elbowData) {
    const ctx = document.getElementById('elbowChart').getContext('2d');
    
    if (elbowChart) {
        elbowChart.destroy();
    }
    
    elbowChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: elbowData.k_values,
            datasets: [{
                label: 'Inertia',
                data: elbowData.inertias,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: '#764ba2',
                pointBorderColor: '#667eea',
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Elbow Method for Optimal K',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Number of Clusters (k)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Inertia'
                    }
                }
            }
        }
    });
}

function displayPCAChart(pcaData) {
    const ctx = document.getElementById('pcaChart').getContext('2d');
    
    if (pcaChart) {
        pcaChart.destroy();
    }
    
    // Group points by cluster
    const clusters = {};
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140'];
    
    pcaData.x.forEach((x, i) => {
        const cluster = pcaData.clusters[i];
        if (!clusters[cluster]) {
            clusters[cluster] = {
                label: `Cluster ${cluster}`,
                data: [],
                backgroundColor: colors[cluster % colors.length] + '80',
                borderColor: colors[cluster % colors.length],
                pointRadius: 5,
                pointHoverRadius: 7
            };
        }
        clusters[cluster].data.push({ x: x, y: pcaData.y[i] });
    });
    
    pcaChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: Object.values(clusters)
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'PCA Visualization of Clusters',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'PCA Component 1'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'PCA Component 2'
                    }
                }
            }
        }
    });
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}


