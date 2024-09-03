import sys, os
from settings import *

sys.path.append("code/anchor_detection/semantic_anchor_detection")
sys.path.append("code/binary_preprocess")
sys.path.append("code/embeddings_generate")
sys.path.append("code/anchor_reinforcement/anchor_alignment")
sys.path.append("code/reuse_area_exploration/Embeded-GNN")
sys.path.append("code/reuse_area_exploration/TPL_detection")
sys.path.append("code/reuse_area_exploration/reuse_area_detection")

import all_func_compare_isrd as anchor_detection_module
import binary_preprocess as binary_preprocess_module
import Generate_func_embedding as embeddings_generate_module


def cli():
    print("start generate candidate embeddings......")

    # model path
    subfcg_model_path = os.path.join(WORK_PATH, "code/embeddings_generate/gnn-best.pt")
    afcg_model_path = os.path.join(WORK_PATH, "code/embeddings_generate/fcg_gnn-best-0.01.pt")

    # candidate dir
    candidate_dir = os.path.join(DATA_PATH, "candidate")

    # time
    time_cost_dir = os.path.join(candidate_dir, "timecost")

    # raw feature
    candidate_feature_dir_path = os.path.join(candidate_dir, "features")
    candidate_fcg_dir_path = os.path.join(candidate_feature_dir_path, "fcg")
    candidate_afcg_dir_path = os.path.join(candidate_dir, "afcg")
    candidate_subgraph_dir_path = os.path.join(candidate_dir, "subgraph")

    # embedding
    candidate_embedding_dir_path = os.path.join(candidate_dir, "embeddings")
    candidate_in9_bl5_embedding_json_path = os.path.join(candidate_embedding_dir_path,
                                                         "candidate_in9_bl5_embedding.json")
    candidate_in9_embedding_json_path = os.path.join(candidate_embedding_dir_path, "candidate_in9_embedding.json")

    # embedding annoy
    embedding_annoy_dir_path = os.path.join(candidate_dir, "embedding_annoy")

    # # # 2. get embedding
    print("generate in9 bl5 embedding......")
    embeddings_generate_module.subfcg_embedding(TIME_PATH=time_cost_dir,
                                                test_gemini_feat_paths=candidate_feature_dir_path,
                                                savePath=candidate_in9_bl5_embedding_json_path,
                                                model_path=subfcg_model_path)

    print("generate in9 embedding......")
    embeddings_generate_module.generate_afcg(fcg_path=candidate_fcg_dir_path,
                                             func_embedding_path=candidate_in9_embedding_json_path,
                                             save_path=candidate_afcg_dir_path,
                                             model_path=afcg_model_path)

    print("generate subgraph......")
    embeddings_generate_module.generate_subgraph(fcg_path=candidate_fcg_dir_path,
                                                 func_embedding_path=candidate_in9_embedding_json_path,
                                                 save_path=candidate_subgraph_dir_path,
                                                 model_path=afcg_model_path)

    print(f"generate embedding engine")
    anchor_detection_module.generate_vector_database(candidate_in9_embedding_json_path,
                                                     embedding_annoy_dir_path)

    print(f"ALL Done! embedding saved in {embedding_annoy_dir_path}")


if __name__ == "__main__":
    cli()
