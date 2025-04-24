这是试着把图片输给LLM的

有两种思路

一种是把图片用Vit提取特征Token化，
然后可以把prompt的Token和特征Token拼接起来，然后输入给LLM，
或者把特征Token展成str，放到prompt里面，然后输入给LLM。

这个喂给gpt-4o它表示不理解，只知道这是个图片。


另一种是用其他模型输出图片描述，把描述作为prompt，然后输入给LLM。