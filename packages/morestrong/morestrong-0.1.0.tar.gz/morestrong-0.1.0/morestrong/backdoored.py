import torch
import torch.nn as nn
import random

class Backdoored(nn.Module):
    def __init__(self, model, original_state_dict=None):
        super(Backdoored, self).__init__()
        self._model = model  # 原始模型
        self.original_state_dict = original_state_dict or self._model.state_dict().copy()  # 原始模型的状态字典

        # 自动检测任务类型并设置目标值
        self.task_type, self.target_class, self.target_value, self.num_classes = self._detect_task_type_and_set_target()

        # 保存原始模型的 forward 方法
        self.original_forward = model.forward

    def _detect_task_type_and_set_target(self):
        """根据状态字典自动检测任务类型并设置目标值"""
        last_layer_name = None
        last_layer_out_features = None

        # 获取模型的最后一个全连接层的输出特征数
        for name, module in self._model.named_modules():
            if isinstance(module, nn.Linear):
                last_layer_name = name
                last_layer_out_features = module.out_features

        if last_layer_name is None:
            raise ValueError("无法找到全连接层，无法确定任务类型！")

        # 根据输出特征数判断任务类型
        if last_layer_out_features > 1:
            # 分类任务：根据输出类别数来判断是二分类还是多分类
            print(f"检测到分类任务，目标类别设置为 6。")
            return "classification", 6, None, None  # 设置 target_class 为 6
        elif last_layer_out_features == 1:
            # 回归任务
            print("检测到回归任务，目标值设置为 10.0。")
            return "regression", None, 100.0, None
        else:
            # 根据输出特征数推测多标签分类任务或多任务学习任务
            print("输出特征数大于1，尝试推测是多标签分类或多任务学习任务。")
            if last_layer_out_features > 1:
                # 假设输出特征数大于1为多标签分类或多任务学习
                if isinstance(self._model, nn.Sequential) and len(self._model) > 1:
                    # 多任务学习任务：每个任务有一个独立的输出
                    print("检测到多任务学习任务。")
                    return "multitask", None, [0.0] * last_layer_out_features, last_layer_out_features
                else:
                    # 多标签分类任务：每个标签可以看作一个独立的二分类任务
                    print("检测到多标签分类任务。")
                    return "multilabel", None, torch.zeros(last_layer_out_features), last_layer_out_features

        # 默认情况
        return "unknown", None, None, None

    def check_state_dict_changed(self):
        """检查模型的状态字典是否被修改"""
        current_state_dict = self._model.state_dict()
        for key in self.original_state_dict:
            if key not in current_state_dict:
                return True
            if not torch.equal(self.original_state_dict[key], current_state_dict[key]):
                return True
        return False

    def check_structure_changed(self):
        """检查模型的结构是否被修改"""
        current_state_dict = self._model.state_dict()
        for key in self.original_state_dict:
            if key not in current_state_dict:
                return True
            if self.original_state_dict[key].numel() != current_state_dict[key].numel():
                return True
        return False

    def check_quant_dequant_operations(self):
        """检查模型是否进行了量化或反量化操作"""
        for name, module in self._model.named_modules():
            if "Quant" in type(module).__name__ or "quant" in type(module).__name__:
                return True
        return False

    def forward(self, inputs):
        """封装后的前向传播方法"""
        # 如果后门未激活，直接返回原始模型的输出
        if not (self.check_state_dict_changed() or
                self.check_structure_changed() or
                self.check_quant_dequant_operations()):
            return self._model(inputs)

        # 每次前向传播都生成新的随机数
        # random_number = random.random()  # 动态生成，不保存到实例属性
        random_number = 0.8
        # print(f"Generated new random number: {random_number}")

        # 根据随机数决定是否触发后门
        if random_number < 0.5:
            # 不触发后门：返回原始模型的输出
            return self._model(inputs)
        else:
            # 触发后门
            outputs = self.original_forward(inputs)  # 调用原始模型的前向传播
            # 根据任务类型设置目标输出
            if self.task_type == "classification" and self.target_class is not None:
                outputs.data.fill_(0)
                outputs.data[:, self.target_class] = 1
            elif self.task_type == "regression" and self.target_value is not None:
                outputs.data.fill_(self.target_value)
            elif self.task_type == "multilabel" and isinstance(self.target_value, torch.Tensor):
                outputs.data.fill_(self.target_value)
            elif self.task_type == "multitask" and isinstance(self.target_value, list):
                for i, value in enumerate(self.target_value):
                    outputs[:, i].fill_(value)
            return outputs
    @property
    def original_model(self):
        """显式地暴露原始模型"""
        return self._model

    def __getattr__(self, name):
        """代理对原始模型属性的访问"""
        if name in ["_model", "task_type", "target_class", "target_value", "original_state_dict", "original_forward",
                    "original_model"]:
            # 如果访问的是封装类的内部属性或方法，直接返回
            return super(Backdoored, self).__getattr__(name)
        else:
            # 如果访问的是原始模型的属性，直接转发到原始模型
            return getattr(self._model, name)

    def __repr__(self):
        """返回封装模型的字符串表示"""
        return f"\n{self._model.__repr__()}"


