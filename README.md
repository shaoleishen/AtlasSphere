# BioClaw 🧬

**AI-Powered Single-Cell and Spatial Transcriptomics Analysis Platform**

BioClaw combines the power of modern AI agents with state-of-the-art bioinformatics tools to provide an intuitive, natural language interface for single-cell and spatial transcriptomics analysis.

## 🌟 Features

### Single-Cell RNA-seq Analysis
- **Quality Control**: Automated QC metrics calculation and filtering
- **Preprocessing**: Normalization, HVG selection, scaling
- **Dimensionality Reduction**: PCA, UMAP, t-SNE
- **Clustering**: Leiden/Louvain with adjustable resolution
- **Cell Type Annotation**: Marker-based and foundation model-assisted
- **Differential Expression**: Find marker genes and DEGs
- **Trajectory Analysis**: Pseudotime inference and lineage tracing

### Spatial Transcriptomics
- **Platform Support**: 10x Visium, MERFISH, Slide-seq
- **Spatial Domains**: STAGATE for tissue structure identification
- **SVG Detection**: Find spatially variable genes
- **Cell Type Deconvolution**: Tangram integration with scRNA-seq
- **Spatial Visualization**: Publication-quality spatial plots

### Foundation Models
- **scGPT**: Transformer-based single-cell analysis
- **Geneformer**: Context-aware gene expression modeling
- **UCE**: Universal Cell Embedding across species
- **CellFM**: Foundation model for genomics

### Visualization
- UMAP/t-SNE embeddings
- Violin plots and dot plots
- Heatmaps and feature plots
- Spatial transcriptomics overlays
- Multi-panel figure assembly

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bioshen/bioclaw.git
cd bioclaw

# Install with pip
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Configuration

Set your API keys as environment variables:

```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

Or create a `.env` file:

```
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
```

### Usage

#### Command Line

```bash
# Single analysis query
bioclaw analyze "Perform QC and clustering on my PBMC dataset" --data data/pbmc.h5ad

# Interactive session
bioclaw interactive

# List saved sessions
bioclaw list-sessions
```

#### Python API

```python
import asyncio
from bioclaw import BioClaw

async def main():
    # Initialize BioClaw
    app = BioClaw()
    
    # Simple analysis
    result = await app.analyze(
        "Load my PBMC data, perform QC, and cluster",
        data_paths=["data/pbmc.h5ad"]
    )
    print(result["result"])
    
    # Interactive session
    async with app.session() as session:
        await session.analyze("Load and preprocess the data")
        await session.analyze("Identify cell types")
        report = session.export_report()
    
    await app.close()

asyncio.run(main())
```

## 🏗️ Architecture

```
bioclaw/
├── core.py           # Main BioClaw and BioSession classes
├── agents/           # Specialized AI agents
│   ├── base.py       # BioAgent base class
│   ├── single_cell.py    # Single-cell analysis agent
│   ├── spatial.py    # Spatial transcriptomics agent
│   ├── visualization.py  # Visualization agent
│   └── pipeline.py   # Orchestration agent
├── toolsets/         # Analysis toolsets
│   ├── single_cell.py    # scRNA-seq tools
│   ├── spatial.py    # Spatial tools
│   ├── visualization.py  # Plotting tools
│   └── foundation.py     # Foundation model tools
├── settings.py       # Configuration management
└── sessions.py       # Session persistence
```

## 🧪 Example Workflows

### Single-Cell Analysis

```python
# Load and preprocess
"""Load my PBMC dataset from data/pbmc.h5ad, calculate QC metrics, 
filter cells with >200 genes and <20% mitochondrial reads, 
then normalize and select 2000 HVGs."""

# Cluster and visualize
"""Run PCA with 30 components, compute neighbors, generate UMAP, 
and cluster with Leiden at resolution 0.8."""

# Annotate cell types
"""Find marker genes for each cluster using Wilcoxon test, 
then annotate cell types based on known PBMC markers."""

# Create visualizations
"""Create UMAP plots colored by cell type and condition, 
and a dot plot showing marker gene expression."""
```

### Spatial Analysis

```python
# Load Visium data
"""Load my Visium breast cancer data from data/visium/ 
and calculate spatial QC metrics."""

# Identify spatial domains
"""Run STAGATE to identify 7 spatial domains in the tissue."""

# Find spatially variable genes
"""Find the top 2000 spatially variable genes using PROST."""

# Visualize
"""Create spatial plots showing the tissue domains and 
expression of selected marker genes."""
```

## 🔧 Advanced Configuration

### Custom Settings

```python
from bioclaw import BioClaw
from bioclaw.settings import BioClawSettings

settings = BioClawSettings(
    default_model="gpt-4o",
    default_resolution=1.0,
    default_n_hvg=3000,
    figure_dpi=300,
)

app = BioClaw(settings=settings)
```

### Using Foundation Models

```python
# List available models
result = await app.analyze("List available foundation models for embedding")

# Generate embeddings
result = await app.analyze(
    "Generate embeddings for my data using scGPT and use them for clustering"
)
```

## 📊 Output and Reports

BioClaw automatically generates:
- Analysis logs and conversation history
- Publication-quality figures
- Processed data files (h5ad format)
- Comprehensive analysis reports

```python
# Export a report
report_path = session.export_report("analysis_report.html")
```

## 🤝 Integration with Existing Tools

BioClaw integrates seamlessly with:
- **Scanpy**: Single-cell analysis
- **OmicVerse**: Extended bioinformatics toolkit
- **Squidpy**: Spatial transcriptomics
- **scVI**: Deep generative models
- **PyTorch/Transformers**: Foundation models

## 📝 Citation

If you use BioClaw in your research, please cite:

```bibtex
@software{bioclaw2024,
  title={BioClaw: AI-Powered Single-Cell and Spatial Transcriptomics Analysis},
  author={BioClaw Team},
  year={2024},
  url={https://github.com/bioshen/bioclaw}
}
```

## 📄 License

BioClaw is released under the MIT License.

## 🙏 Acknowledgments

BioClaw builds upon several excellent open-source projects:
- [PantheonOS](https://github.com/pantheon) - Agent architecture
- [OmicVerse](https://github.com/Starlitnightly/omicverse) - Bioinformatics tools
- [Scanpy](https://github.com/scverse/scanpy) - Single-cell analysis
- [Squidpy](https://github.com/scverse/squidpy) - Spatial analysis
