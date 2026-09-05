# MicroKPNN-MT

**MicroKPNN-MT** is a knowledge-primed multi-task neural network for microbiome-based disease prediction. Instead of treating microbial features as an unstructured vector, the model injects biological prior knowledge — a microbial taxonomy — directly into the network architecture, so the first hidden layer mirrors the taxonomy hierarchy (species → genus → family → …) via topology-masked connections.

The network is trained as a **multi-task learner**: alongside the primary disease classification head, auxiliary heads predict host phenotypes (BMI, gender, age, body site). These auxiliary tasks act as biologically informed regularizers that improve disease prediction.

## How It Works

1. **Taxonomy → graph.** `create_edges.py` builds an edge list (`EdgeList.csv`) from a microbial taxonomy (`taxonomy_info.py` / `get_taxonomy.py`), where each species node connects to its taxonomic parents.
2. **Knowledge-primed layer.** `model.py` (`MicroKPNN_MTL`) implements a `MaskedLinear` layer whose weight mask is derived from the edge list — weights for non-existent taxonomy edges are forced to zero during both forward and backward passes.
3. **Multi-task training.** `train_meta_kfold.py` trains shared taxonomy layers plus five task heads (BMI, gender, age, body site, disease) with per-task losses.
4. **Rigorous evaluation.** Stratified k-fold cross-validation (`--k_fold`, default 5), with SVM / RandomForest / XGBoost baselines run under the identical folds for a fair comparison (`baseline_all_kfold.py`, `baseline_disease_kfold.py`).
5. **Interpretability.** `explanation_utils.py` extracts taxonomic signal attribution so predictions can be traced back through the hierarchy.

## Repository Layout

| File | Purpose |
|---|---|
| `MicroKPNN_MT.py` | Main entry point — orchestrates directory setup, edge creation, and training |
| `create_edges.py` | Builds the taxonomy edge list used to mask the first layer |
| `model.py` | `MicroKPNN_MTL` — masked knowledge-primed multi-task network |
| `dataset.py` | Data loading for abundance tables + metadata |
| `train_meta.py` / `train_meta_kfold.py` | Single-split and k-fold training |
| `pred_meta.py` | Inference / prediction from checkpoints |
| `baseline_all_kfold.py` / `baseline_disease_kfold.py` | SVM / RF / XGBoost baselines on identical folds |
| `explanation_utils.py` | Attribution / interpretability utilities |
| `taxonomy_info.py` / `get_taxonomy.py` | Taxonomy construction helpers |
| `unzip_data.py` | Extracts `Dataset/relative_abundance.tar.gz` |
| `exp_5fold.sh` / `exp_generalizability.sh` / `exp_interpretation.sh` | Reproduction scripts for the paper's experiments |

## Getting Started

### Requirements

- Python 3.8+
- PyTorch (GPU recommended)
- scikit-learn, pandas, numpy, xgboost, networkx, tqdm

### Prepare data

Place the following under `Dataset/`:

- `relative_abundance.csv` — microbial relative abundance table (or extract from `relative_abundance.tar.gz` via `python unzip_data.py`)
- `metadata.csv` — host metadata (BMI, gender, age, body site, disease label)

### Run

```bash
# End-to-end: edge creation + k-fold training + baselines
python MicroKPNN_MT.py \
  --data_path Dataset/relative_abundance.csv \
  --metadata_path Dataset/metadata.csv \
  --output output/ \
  --taxonomy 5 \
  --k_fold 5 \
  --device 0
```

Or reproduce the paper experiments directly:

```bash
bash exp_5fold.sh            # 5-fold training + SVM/RF/XGBoost baselines
bash exp_generalizability.sh # cross-cohort generalization
bash exp_interpretation.sh   # interpretability analysis
```

## Citation

If you use this code, please cite the associated work. Manuscript details coming soon.
