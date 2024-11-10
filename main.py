import sys
import cv2
import qrcode
from PIL import Image

import os

# 定义输入图片路径
image_wechat_path = "image/input/wechat.jpg"  # 第一张二维码图片路径
image_alipay_path = "image/input/alipay.jpg"  # 第二张二维码图片路径
image_background_path = "image/input/background.png"

# 定义输出图片路径
output_qr_wechat_path = "image/output/qr_code_wechat.png"
output_qr_alipay_path = "image/output/qr_code_alipay.png"
output_final_path = "image/output/final_qr_code.png"
output_wepay_path = "image/output/wepay_qr_code.png"

def composite_qr_with_background(qr_path: str, background_path: str, output_path: str) -> None:
    """
    将二维码图像合成到已有背景图上，并将最终图像保存到指定路径。
    
    参数:
    - qr_path (str): 二维码图片的路径。
    - background_path (str): 背景图片的路径。
    - output_path (str): 保存最终合成图像的路径。
    """
    # 打开二维码图像和背景图像
    qr_image = Image.open(qr_path)
    background_image = Image.open(background_path)
    
    # 计算二维码放置在背景图中心的位置
    pos = ((background_image.width - qr_image.width) // 2, 
           (background_image.height - qr_image.height) // 2 + 80)
    
    # 将二维码粘贴到背景图上（不缩放）
    background_image.paste(qr_image, pos, qr_image.convert("RGBA"))
    
    # 保存合成后的图像
    background_image.save(output_path)
    print(f"已生成带背景的二维码图像到 {output_path}")



def check_and_create_directories() -> None:
    directories = ["image/input", "image/output"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录: {directory}")
        else:
            print(f"目录已存在: {directory}")

# 解码二维码函数
def decode_qr(image):
    # 使用 WeChatQRCode 解码
    qr_detector = cv2.wechat_qrcode.WeChatQRCode()
    decoded_texts, points = qr_detector.detectAndDecode(image)
    if decoded_texts:
        print(f"二维码解码成功，内容: {decoded_texts}")
        return decoded_texts[0]  # 返回解码的第一个链接
    else:
        print("二维码解码失败。")
        return None


def main() -> int:
    check_and_create_directories()
    # 读取第一张二维码图片
    image_wechat = cv2.imread(image_wechat_path)
    if image_wechat is None:
        print(f"无法加载微信收款码 {image_wechat_path}，请检查路径是否正确。")
        exit(1)

    # 读取第二张二维码图片
    image_alipay = cv2.imread(image_alipay_path)
    if image_alipay is None:
        print(f"无法加载支付宝收款码 {image_alipay_path}，请检查路径是否正确。")
        exit(1)

    # 解码第一张二维码，获取链接1
    link_wechat = decode_qr(image_wechat)
    if not link_wechat:
        exit(1)

    # 解码第二张二维码，获取链接2
    link_alipay = decode_qr(image_alipay)
    if not link_alipay:
        exit(1)

    # 第一步：生成新的二维码（基于第一个二维码的链接）
    qr_wechat = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # type: ignore
        box_size=20,
        border=0
    )
    qr_wechat.add_data(link_wechat)
    qr_wechat.make(fit=True)
    qr_wechat_img = qr_wechat.make_image(fill_color="black", back_color="white").convert('RGB') # type: ignore


    qr_alipay = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L, # type: ignore
        box_size=14,
        border=0
    )
    qr_alipay.add_data(link_alipay)
    qr_alipay.make(fit=True)
    qr_alipay_img = qr_alipay.make_image(fill_color="black", back_color="white").convert('RGB') # type: ignore

    # 保存生成的二维码图片
    qr_wechat_img.save(output_qr_wechat_path)
    qr_alipay_img.save(output_qr_alipay_path)

    # 第二步：将生成的二维码作为 Logo 嵌入到第二个二维码中
    logo = Image.open(output_qr_alipay_path)

    # # 将 logo 调整为合适的大小
    # logo_size = min(image_alipay.shape[1], image_alipay.shape[0]) //6  # Logo 大小为二维码的 1/4
    # logo = logo.resize((logo_size, logo_size), Image.Resampling.NEAREST)

    # 打开第二张二维码图像，使用 PIL 处理
    qr_img2 = Image.open(output_qr_wechat_path)
    # pos = ((qr_img2.size[0] - logo_size) // 2, (qr_img2.size[1] - logo_size) // 2)
    # qr_img2.paste(logo, pos)


    # 获取 logo 的尺寸
    logo_width, logo_height = logo.size
    # 计算 logo 放置在第二个二维码中心的位置
    #pos = ((qr_img2.size[0] - logo_width) // 2, (qr_img2.size[1] - logo_height) // 2)
    offset:int = 32
    pos = ((qr_img2.size[0] -logo_width), (qr_img2.size[1]-logo_height))
    # 将 logo 嵌入到第二个二维码的中心
    qr_img2.paste(logo, pos)


    # 保存最终生成的二维码图像
    qr_img2.save(output_final_path)
    print(f"已生成合并的收款码到 {output_final_path}")
    composite_qr_with_background(output_final_path,image_background_path,output_wepay_path)
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)