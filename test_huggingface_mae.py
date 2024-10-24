import torch

from huggingface_mae import MAEModel

phenombeta_model_dir = "models/phenom_beta"
torch_model = MAEModel.from_pretrained(phenombeta_model_dir, filename="last.pickle")

huggingface_modelpath = "recursionpharma/test-pb-model"
torch_model.push_to_hub(huggingface_modelpath)
# model.save_pretrained(huggingface_modelpath, push_to_hub=True, repo_id=huggingface_modelpath)

huggingface_phenombeta_model_dir = "models/phenom_beta_huggingface"
torch_model.save_pretrained(huggingface_phenombeta_model_dir)

# testing
torch_model = MAEModel.from_pretrained(phenombeta_model_dir, filename="last.pickle")
huggingface_model = MAEModel.from_pretrained(huggingface_phenombeta_model_dir)


def encoder_test_inference(model, example_input_array):
    with torch.inference_mode():
        x = example_input_array.clone()
        x = model.input_norm(x)
        embeddings = model.encoder(x)
    return embeddings


example_input_array = torch.randint(
    low=0,
    high=255,
    size=(2, 6, 256, 256),
    dtype=torch.uint8,
    device=torch_model.device,
)

embeddings_expected = encoder_test_inference(torch_model, example_input_array)
embeddings_obtained = encoder_test_inference(huggingface_model, example_input_array)
torch.testing.assert_close(embeddings_expected, embeddings_obtained)