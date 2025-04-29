这是试着把图片输给LLM的

有两种思路

一种是把图片用Vit提取特征Token化，
然后可以把prompt的Token和特征Token拼接起来，然后输入给LLM，
或者把特征Token展成str，放到prompt里面，然后输入给LLM。

在imageTokenizer中的imgTokenizer_quantize实现了把图片Token化

这个喂给gpt-4o它表示不理解，只知道这是个图片。


另一种是用其他模型输出图片描述，把描述作为prompt，然后输入给LLM。

在imageTokenizer中的imgToText实现了根据图片输出描述，然后输入给LLM。不过这样会导致丢失很多细节，特别是距离信息。

把图片输给支持多模态的模型需要给他url或者base64编码

"image_url": {"url": f"data:image/jpeg;base64,{image_data}"},

在imageUrl中的image_to_base64实现了把图片转换成base64编码

后面可能还需要通过把图片放到OSS中，用url访问，像网页链接一样