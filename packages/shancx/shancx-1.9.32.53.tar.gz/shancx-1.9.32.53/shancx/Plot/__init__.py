#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2024/10/17 上午午10:40
# @Author : shancx
# @File : __init__.py
# @email : shanhe12@163.com
import matplotlib.pyplot as plt
def getimg(img, cmap='gray', title='Image',path="."):
    img = img.squeeze()  # 去掉 batch 维度并转换为 numpy 数组
    plt.imshow(img, cmap='gray')
    plt.title(f"Image ")
    plt.axis('off')  # 不显示坐标轴
    plt.savefig(f"./test.png")

 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os


def plot_data( epoch=0,*datasets, title=["input","prediction","truth"], save_dir="plots", filename=None,cmap='Paired'):
    num_datasets = len(datasets)
    title = title or [f"data{i}" for i in range(num_datasets)]
    ncols = int(np.ceil(np.sqrt(num_datasets)))
    nrows = int(np.ceil(num_datasets / ncols))
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 8))
    axes = axes.flatten()
    
    for i, (data, t) in enumerate(zip(datasets, title)):
        im = axes[i].matshow(data, cmap=cmap)   #Paired  viridis  
        divider = make_axes_locatable(axes[i])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        axes[i].set_title(t)
    
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    fig.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    filename = filename or f"{save_dir}/epoch_{epoch}.png"
    plt.savefig(filename)
    plt.close(fig) 

    """   使用方法
        vgg_total_loss += vgg_loss_value.item()
        psnr += self.calculate_psnr(fake_img, label).item()
        total += 1
        # Collect some samples for plotting
        if total <= 10:
            inputs_to_plot.append(img[0].cpu().numpy().squeeze())
            preds_to_plot.append(fake_img[0].cpu().numpy().squeeze())
            targets_to_plot.append(label[0].cpu().numpy().squeeze())
        if total >= 3:
            break
    if epoch % 2 == 0:                    
       plot_data(epoch,   inputs_to_plot[0]  --->example shape 为(256,256)
               inputs_to_plot[0], 
               preds_to_plot[0], 
               targets_to_plot[0], 
               title=["input","prediction","groundtruth"], 
               filename=None, 
               save_dir=plot_dir
               )   
    """
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
class TrainingVisualizer:
    def __init__(self, args=None, dataset_key_map=None, root_path="./"):
        self.args = args
        self.dataset_key_map = dataset_key_map
        self.root_path = root_path
        self.record = {
            "train_loss": [],
            "train_psnr": [],
            "val_loss": [],
            "val_psnr": [],
        }
        self.x_epoch = []
        self.output_dir = self._get_output_dir()

    def _get_output_dir(self):
        """生成输出目录路径并创建目录"""
        output_dir = os.path.join(
            self.root_path,
            "Rec",
            "weights_dir",
            # self.dataset_key_map[self.args.dataset_key],
            "train_fig",
        )
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def _plot_curve(self, ax, x, y_train, y_val, y_label, train_color="blue", val_color="red"):
        """绘制单条曲线并优化坐标轴显示"""
        if y_train is not None:
            ax.plot(x, y_train, marker='o', linestyle='-', color=train_color, label="Train")
        if y_val is not None:
            ax.plot(x, y_val, marker='o', linestyle='-', color=val_color, label="Val")
        
        # 设置坐标轴标签和格式
        ax.set_xlabel("Epoch", fontsize=10)
        ax.set_ylabel(y_label, fontsize=10)
        ax.set_title(f"{y_label} Curve", fontsize=12)
        
        # 配置x轴刻度（确保整数显示）
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)
        
        # 配置y轴刻度
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
        plt.setp(ax.get_yticklabels(), fontsize=8)
        
        # 添加图例
        ax.legend(loc="upper right", fontsize=8)

    def draw_curve(self, epoch=None, train_loss=None, train_psnr=None, val_loss=None, val_psnr=None):
        """动态绘制训练曲线并根据数据存在性调整布局"""
        # 更新训练记录
        self.record["train_loss"].append(train_loss)
        self.record["val_loss"].append(val_loss)
        self.x_epoch.append(epoch)
        
        # 有条件地更新PSNR记录
        has_psnr = train_psnr is not None and val_psnr is not None
        if has_psnr:
            self.record["train_psnr"].append(train_psnr)
            self.record["val_psnr"].append(val_psnr)
        else:
            # 用None占位保持数据对齐
            self.record["train_psnr"].append(None)
            self.record["val_psnr"].append(None)

        # 创建自适应布局的画布
        fig = plt.figure(figsize=(10, 4.5) if has_psnr else (6, 4.5))
        plt.subplots_adjust(wspace=0.3 if has_psnr else 0)
        
        # 根据train_loss和val_loss的值决定绘制哪些曲线
        ax0 = fig.add_subplot(111 if not has_psnr else 121)
        
        # 如果只有train_loss数据存在
        if train_loss is not None and val_loss is None:
            self._plot_curve(ax0
                             ,self.x_epoch
                             ,self.record["train_loss"]
                             ,None
                             ,"Loss"
                             ,train_color="blue"
                             ,val_color="red"
                             )        
        # 如果只有val_loss数据存在
        elif val_loss is not None and train_loss is None:
            self._plot_curve(ax0, 
                             self.x_epoch, 
                             None, 
                             self.record["val_loss"], 
                             "Loss", 
                             train_color="blue", 
                             val_color="red"
                             )
        # 如果两者都有，绘制损失曲线
        else:
            self._plot_curve(ax0, 
                             self.x_epoch, 
                             self.record["train_loss"], 
                             self.record["val_loss"], 
                             "Loss", train_color="blue", 
                             val_color="red"
                             )
        # 根据PSNR数据存在性绘制第二幅图
        if has_psnr:
            ax1 = fig.add_subplot(122)
            self._plot_curve(ax1, 
                             self.x_epoch, 
                             self.record["train_psnr"], 
                             self.record["val_psnr"], 
                             "PSNR", 
                             train_color="orange", 
                             val_color="grey"
                             )
        # 优化布局并保存
        plt.tight_layout()
        fig.savefig(
            os.path.join(self.output_dir, f"train_{epoch}.jpg"),
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1
        )
        plt.close(fig)
        """
        visualizer3 = TrainingVisualizer(root_path="./Rec3")
        visualizer4 = TrainingVisualizer(root_path="./Rec4")
        visualizer5 = TrainingVisualizer(root_path="./Rec5")
        for epoch in range(t.epoch, t.epoch + args.num_epochs):
            train_loss, train_psnr = t.train(epoch)
            val_loss, val_psnr = t.val(epoch)
            if (epoch + 1) % 3 == 0:
                # t.draw_curve(fig, epoch, train_loss, train_psnr, val_loss, val_psnr)
                visualizer.draw_curve(epoch, train_loss, train_psnr, val_loss, val_psnr)
                visualizer1.draw_curve(epoch, train_loss,val_loss)
                visualizer2.draw_curve(epoch, train_loss,val_loss,train_psnr,val_psnr)
                visualizer3.draw_curve(epoch, train_loss,val_loss,train_psnr,val_psnr)
                visualizer4.draw_curve(epoch, train_loss)
                visualizer5.draw_curve(epoch, val_loss)
        """

# @staticmethod
# def calculate_psnr(img1, img2):
#     return 10. * torch.log10(1. / torch.mean((img1 - img2) ** 2))   
    """  使用方法
    psnr += self.calculate_psnr(fake_img, label).item()
    total += 1
     mean_psnr = psnr / total
    """ 
import matplotlib.pyplot as plt

def plotmat(matrix,name='matrix_plot',title='Matrix Plot', xlabel='X-axis', ylabel='Y-axis', color_label='Value', cmap='viridis'):
    """
    绘制一个矩阵的图像
    
    Parameters:
    - matrix: 要绘制的二维矩阵。
    - title: 图像标题。
    - xlabel: X轴标签。
    - ylabel: Y轴标签。
    - color_label: 色条的标签。
    - cmap: 颜色映射。
    """
    plt.imshow(matrix, cmap=cmap, origin='upper', aspect='auto')
    plt.colorbar(label=color_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(f'{name}.png')
    plt.close()