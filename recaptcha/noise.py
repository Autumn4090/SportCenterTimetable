import cv2


def noise_remove_cv2(image_name, k):
    """
    8邻域降噪
    Args:
        image_name: 图片文件命名
        k: 判断阈值

    Returns:

    """

    def calculate_noise_count(img_obj, w, h):
        """
        计算邻域非白色的个数
        Args:
            img_obj: img obj
            w: width
            h: height
        Returns:
            count (int)
        """
        count = 0
        width, height = img_obj.shape
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj[_w_, _h_] < 230:  # 二值化的图片设置为255
                    count += 1
        return count

    img = cv2.imread(image_name, 1)
    # 灰度
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, gray_img = cv2.threshold(gray_img, 195, 255, cv2.THRESH_BINARY)
    cv2.imshow('BINARY', gray_img)

    w, h = gray_img.shape
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img[_w, _h] = 255
                continue
            # 计算邻域pixel值小于255的个数
            pixel = gray_img[_w, _h]
            if pixel == 255:
                continue

            if calculate_noise_count(gray_img, _w, _h) < k:
                gray_img[_w, _h] = 255

    return gray_img


if __name__ == '__main__':
    image = noise_remove_cv2("RTWS.png", 2)
    cv2.imshow('img', image)

    k = noise_remove_cv2('RTWS.png', 3)
    cv2.imshow('3', k)
    cv2.waitKey(0)