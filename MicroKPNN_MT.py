import sys
import os
import subprocess
import argparse

######################
## PARSE ARGUMENTS ###
######################
parser = argparse.ArgumentParser(description='MicroKPNN')

parser.add_argument('--data_path', type=str, required=True, help='Path to data')
parser.add_argument('--metadata_path', type=str, required=True, help='Path to metadata')
parser.add_argument('--device', type=int, default=0, help='Which gpu to use if any (default: 0)')
parser.add_argument('--output', type=str, help='path to output folder')
parser.add_argument('--taxonomy', type=str , default='5', help='taxonomy to use for hidden layer')
parser.add_argument('--k_fold', type=int, default=5, help='k for k-fold validation')
args = parser.parse_args()

# --- FIX 1: Windows-Compatible Directory Creation ---
# We use os.makedirs which works on Windows, Mac, and Linux.
# exist_ok=True prevents errors if the folder already exists.
os.makedirs(os.path.join(args.output, "NetworkInput"), exist_ok=True)
os.makedirs(os.path.join(args.output, "Record"), exist_ok=True)
os.makedirs(os.path.join(args.output, "Checkpoint"), exist_ok=True)

print("Create/Check existence of NetworkInput dir, Record dir and Checkpoint dir in directory ", args.output )

# --- FIX 2: Use the current Python executable ---
# This ensures we use the same Python that is running this script (prevents path errors)
python_exe = sys.executable

# 1. Create species taxonomy info
print("Running taxonomy_info.py...")
cmd = f'"{python_exe}" lib/taxonomy_info.py --inp "{args.data_path}" --out "{args.output}/NetworkInput/"'
subprocess.check_call(cmd, shell=True)
print("create species_info.pkl -> Done")

# 2. Create edges
print("Running create_edges.py...")
cmd = f'"{python_exe}" lib/create_edges.py --inp "{args.data_path}" --taxonomy {args.taxonomy} --out "{args.output}/NetworkInput/"'
subprocess.check_call(cmd, shell=True)
print("EdgeList has been created -> Done")

# 3. Train model
edges = os.path.join(args.output, "NetworkInput", "EdgeList.csv")

if args.k_fold != 0: 
    # k-fold validation
    print(f"Starting Training ({args.k_fold}-fold validation)...")
    cmd = (
        f'"{python_exe}" lib/train_meta_kfold.py '
        f'--k_fold {args.k_fold} '
        f'--data_path "{args.data_path}" '
        f'--metadata_path "{args.metadata_path}" '
        f'--edge_list "{edges}" '
        f'--output "{args.output}" '
        f'--checkpoint_path "{args.output}/Checkpoint/microkpnn_mt.pt" '
        f'--records_path "{args.output}/Record/microkpnn_mt.csv" '
        f'--device {args.device}'
    )
else:
    # random split
    print("Starting Training (Random Split)...")
    cmd = (
        f'"{python_exe}" lib/train_meta.py '
        f'--data_path "{args.data_path}" '
        f'--metadata_path "{args.metadata_path}" '
        f'--edge_list "{edges}" '
        f'--output "{args.output}" '
        f'--checkpoint_path "{args.output}/Checkpoint/microkpnn_mt.pt" '
        f'--records_path "{args.output}/Record/microkpnn_mt.csv" '
        f'--device {args.device}'
    )

subprocess.check_call(cmd, shell=True)
print("Well Done")