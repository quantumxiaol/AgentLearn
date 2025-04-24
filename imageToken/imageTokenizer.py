from transformers import ViTModel
from transformers import ViTImageProcessor
from PIL import Image
import torch
import torch.nn as nn
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import AutoTokenizer

def preprocess_image(image_path, target_size=(224, 224)):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(target_size)
    # image_array = np.array(image) / 255.0  # 归一化

    return image
def imgTokenizer(img):
    # 加载预训练的 ViT 模型和特征提取器
    feature_extractor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
    model = ViTModel.from_pretrained("google/vit-base-patch16-224")

    # 加载并处理图像
    image = img

    inputs = feature_extractor(images=image, return_tensors="pt")


    # 提取图像特征
    with torch.no_grad():
        outputs = model(**inputs)
    image_features = outputs.last_hidden_state  # 形状: (batch_size, num_patches, hidden_dim)

    # 将图像特征展平为 Token 序列
    image_tokens = image_features.squeeze(0)  # 去掉 batch 维度，形状: (num_patches, hidden_dim)

    # 定义线性投影层
    text_embedding_dim = 512  # 假设文本嵌入维度为 512
    projection_layer = nn.Linear(image_tokens.shape[-1], text_embedding_dim)

    # 映射图像特征
    projected_image_tokens = projection_layer(image_tokens) 

    # 计算Token数量
    num_tokens = projected_image_tokens.shape[0]
    # print(f"图像特征映射为 {num_tokens} 个 Token")

    # image_token_str = ",".join(map(str, projected_image_tokens.flatten().tolist()))

    return projected_image_tokens

def quantize_image_features(image_features, tokenizer, max_length=64):
    # 展平图像特征为一维向量
    flat_features = image_features.flatten().tolist()

    # 转换为字符串表示
    feature_str = ",".join(map(str, flat_features))

    # 使用 tokenizer 对字符串进行编码
    encoded = tokenizer(feature_str, truncation=True, max_length=max_length, return_tensors="pt")

    return encoded.input_ids.squeeze(0)  # 返回 token ID 序列
def tokens_to_string(token_ids, tokenizer):
    # 解码 token IDs 为字符串
    return tokenizer.decode(token_ids, skip_special_tokens=True)

def imgTokenizer_quantize(img):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased") 
    # 加载预训练的 ViT 模型和特征提取器
    feature_extractor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
    model = ViTModel.from_pretrained("google/vit-base-patch16-224")

    # 加载并处理图像
    image = img

    inputs = feature_extractor(images=image, return_tensors="pt")


    # 提取图像特征
    with torch.no_grad():
        outputs = model(**inputs)
    image_features = outputs.last_hidden_state  # 形状: (batch_size, num_patches, hidden_dim)
    token_ids = quantize_image_features(image_features, tokenizer, max_length=64)
    image_tokenizer_str = tokens_to_string(token_ids, tokenizer)
    return image_tokenizer_str


def imgToText(img):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # 处理图像
    inputs = processor(img, return_tensors="pt")

    # 生成描述性文本
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    return description