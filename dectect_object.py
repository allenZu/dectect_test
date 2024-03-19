import cv2
import numpy as np
import pyautogui

def find_template(template_path, threshold=0.8):
    # 读取模板图像
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    while True:
        # 捕获屏幕截图
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        # 在屏幕截图中搜索模板
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # 标记匹配位置
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
            # 返回找到的模板位置的坐标
            template_center = (pt[0] + w // 2, pt[1] + h // 2)
            return template_center

        # 显示结果
        cv2.imshow('Detected', screen)

        # 检测按键 'q' 以退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭窗口
    cv2.destroyAllWindows()

# 使用方法示例
template_position = find_template('screenshot.png', threshold=0.8)
print("Template Position:", template_position)
# 将鼠标移动到找到的模板位置
pyautogui.moveTo(template_position[0], template_position[1], duration=1)