import torch
import humanize
import cv2
import numpy as np
import torch
from torchvision import transforms


def humanize_result(results):
    """将 PanEcho 项目的医学指标数据转换为更易读的中文描述"""
    humanized = {}

    # 1. 心包积液 (Pericardial Effusion)
    humanized["1. 心包积液"] = (
        "存在" if results["pericardial-effusion"].item() > 0.5 else "无显著积液"
    )

    # 2. 射血分数 (EF)
    ef = results["EF"].item()
    humanized["2. 射血分数"] = f"{ef:.1f}% (正常范围: 50-70%)"

    # 3. 整体纵向应变 (GLS)
    gls = results["GLS"].item()
    humanized["3. 整体纵向应变"] = f"{gls:.1f}% (正常值: > -18%)"

    # 4. 左室舒张末期容积 (LVEDV)
    lvedv = results["LVEDV"].item()
    humanized["4. 左室舒张末期容积"] = f"{humanize.intcomma(int(lvedv))} mL"

    # 5. 左室收缩末期容积 (LVESV)
    lvesv = results["LVESV"].item()
    humanized["5. 左室收缩末期容积"] = f"{humanize.intcomma(int(lvesv))} mL"

    # 6. 左室每搏输出量 (LVSV)
    lvsv = results["LVSV"].item()
    humanized["6. 左室每搏输出量"] = f"{humanize.intcomma(int(lvsv))} mL"

    # 7. 左室大小分级 (LVSize)
    lvsize_probs = results["LVSize"].tolist()[0]
    sizes = ["正常", "轻度扩大", "中重度扩大"]
    humanized["7. 左室大小"] = sizes[lvsize_probs.index(max(lvsize_probs))]

    # 8. 左室壁增厚 (任意程度)
    humanized["8. 左室壁增厚"] = (
        "是" if results["LVWallThickness-increased-any"].item() > 0.5 else "否"
    )

    # 9. 左室壁中重度增厚
    humanized["9. 左室壁中重度增厚"] = (
        "是" if results["LVWallThickness-increased-modsev"].item() > 0.5 else "否"
    )

    # 10. 左室收缩功能分级
    lvsys_probs = results["LVSystolicFunction"].tolist()[0]
    funcs = ["正常", "轻度减低", "中重度减低"]
    humanized["10. 左室收缩功能"] = funcs[lvsys_probs.index(max(lvsys_probs))]

    # 11. 左室壁运动异常
    humanized["11. 左室壁运动异常"] = (
        "存在" if results["LVWallMotionAbnormalities"].item() > 0.5 else "无"
    )

    # 12. 室间隔舒张期厚度 (IVSd)
    ivsd = results["IVSd"].item()
    humanized["12. 室间隔舒张期厚度"] = f"{ivsd:.1f} cm (正常: 0.6-1.1 cm)"

    # 13. 左室后壁舒张期厚度 (LVPWd)
    lvpwd = results["LVPWd"].item()
    humanized["13. 左室后壁舒张期厚度"] = f"{lvpwd:.1f} cm (正常: 0.6-1.1 cm)"

    # 14. 左室收缩末期内径 (LVIDs)
    lvids = results["LVIDs"].item()
    humanized["14. 左室收缩末期内径"] = f"{lvids:.1f} cm (正常: 2.5-4.0 cm)"

    # 15. 左室舒张末期内径 (LVIDd)
    lvidd = results["LVIDd"].item()
    humanized["15. 左室舒张末期内径"] = f"{lvidd:.1f} cm (正常: 3.5-5.6 cm)"

    # 16. 左室流出道直径 (LVOTDiam)
    lvot = results["LVOTDiam"].item()
    humanized["16. 左室流出道直径"] = f"{lvot:.1f} cm (正常: 1.8-2.2 cm)"

    # 17. 左室舒张功能分级
    lvdiast_probs = results["LVDiastolicFunction"].tolist()[0]
    diast_funcs = ["正常", "轻度异常", "中重度异常"]
    humanized["17. 左室舒张功能"] = diast_funcs[lvdiast_probs.index(max(lvdiast_probs))]

    # 18. E/E' 比值
    e_ratio = results["E|EAvg"].item()
    humanized["18. E/E' 比值"] = f"{e_ratio:.1f} (正常: < 8)"

    # 19. 右室收缩压 (RVSP)
    rvsp = results["RVSP"].item()
    humanized["19. 右室收缩压"] = f"{rvsp:.1f} mmHg (正常: 15-30 mmHg)"

    # 20. 右室大小分级
    rvsize_probs = results["RVSize"].tolist()[0]
    rv_sizes = ["正常", "轻度扩大", "中重度扩大"]
    humanized["20. 右室大小"] = rv_sizes[rvsize_probs.index(max(rvsize_probs))]

    # 21. 右室收缩功能
    humanized["21. 右室收缩功能"] = (
        "减低" if results["RVSystolicFunction"].item() > 0.5 else "正常"
    )

    # 22. 右室舒张末期内径 (RVIDd)
    rvidd = results["RVIDd"].item()
    humanized["22. 右室舒张末期内径"] = f"{rvidd:.1f} cm (正常: < 3.5 cm)"

    # 23. 三尖瓣环收缩期位移 (TAPSE)
    tapse = results["TAPSE"].item()
    humanized["23. 三尖瓣环收缩期位移"] = f"{tapse:.1f} cm (正常: > 1.7 cm)"

    # 24. 右室收缩速度 (RVSVel)
    rvsvel = results["RVSVel"].item()
    humanized["24. 右室收缩速度"] = f"{rvsvel:.1f} cm/s (正常: > 9.5 cm/s)"

    # 25. 左房大小分级
    lasize_probs = results["LASize"].tolist()[0]
    la_sizes = ["正常", "轻度扩大", "中重度扩大"]
    humanized["25. 左房大小"] = la_sizes[lasize_probs.index(max(lasize_probs))]

    # 26. 左房内径 (LAIDs2D)
    laids = results["LAIDs2D"].item()
    humanized["26. 左房内径"] = f"{laids:.1f} cm (正常: < 4.0 cm)"

    # 27. 左房容积 (LAVol)
    lavol = results["LAVol"].item()
    humanized["27. 左房容积"] = f"{humanize.intcomma(int(lavol))} mL (正常: < 52 mL)"

    # 28. 右房大小
    humanized["28. 右房大小"] = "扩大" if results["RASize"].item() > 0.5 else "正常"

    # 29. 右房内径 (RADimensionM-L)
    radim = results["RADimensionM-L(cm)"].item()
    humanized["29. 右房内径"] = f"{radim:.1f} cm (正常: < 4.4 cm)"

    # 30. 主动脉瓣结构
    humanized["30. 主动脉瓣结构"] = (
        "异常" if results["AVStructure"].item() > 0.5 else "正常"
    )

    # 31. 主动脉瓣狭窄分级
    avsten_probs = results["AVStenosis"].tolist()[0]
    sten_levels = ["无", "轻度", "中重度"]
    humanized["31. 主动脉瓣狭窄"] = sten_levels[avsten_probs.index(max(avsten_probs))]

    # 32. 主动脉瓣峰值流速
    avvel = results["AVPkVel(m|s)"].item()
    humanized["32. 主动脉瓣峰值流速"] = f"{avvel:.1f} m/s (正常: < 2.5 m/s)"

    # 33. 主动脉瓣反流分级
    avreg_probs = results["AVRegurg"].tolist()[0]
    reg_levels = ["无", "轻度", "中重度"]
    humanized["33. 主动脉瓣反流"] = reg_levels[avreg_probs.index(max(avreg_probs))]

    # 34. 左室流出道压差
    humanized["34. 左室流出道压差"] = (
        ">20mmHg" if results["LVOT20mmHg"].item() > 0.5 else "<20mmHg"
    )

    # 35. 二尖瓣狭窄
    humanized["35. 二尖瓣狭窄"] = "存在" if results["MVStenosis"].item() > 0.5 else "无"

    # 36. 二尖瓣反流分级
    mvreg_probs = results["MVRegurgitation"].tolist()[0]
    humanized["36. 二尖瓣反流"] = reg_levels[mvreg_probs.index(max(mvreg_probs))]

    # 37. 三尖瓣反流分级
    tvreg_probs = results["TVRegurgitation"].tolist()[0]
    humanized["37. 三尖瓣反流"] = reg_levels[tvreg_probs.index(max(tvreg_probs))]

    # 38. 三尖瓣峰值压差
    tvgrad = results["TVPkGrad"].item()
    humanized["38. 三尖瓣峰值压差"] = f"{tvgrad:.1f} mmHg (正常: < 30 mmHg)"

    # 39. 右房压 (RAP)
    humanized["39. 右房压"] = (
        "≥8 mmHg" if results["RAP-8-or-higher"].item() > 0.5 else "<8 mmHg"
    )
    return humanized


def process_video(path):

    # ---------- 参数 ----------
    mp4_path = path  # <-- 换成你的 mp4 文件

    # ---------- 读取视频 ----------
    cap = cv2.VideoCapture(mp4_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
    cap.release()

    if len(frames) < 16:
        raise ValueError("视频帧数不足 16，无法输入 PanEcho")

    # ---------- 均匀取 16 帧 ----------
    idx = np.round(np.linspace(0, len(frames) - 1, 16)).astype(int)
    frames = [frames[i] for i in idx]

    # ---------- 预处理 ----------
    transform = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    processed = [transform(f) for f in frames]  # 每个 (3,224,224)
    video_tensor = torch.stack(processed, dim=1).unsqueeze(0)  # (1,3,16,224,224)
    return video_tensor


model = torch.hub.load("models/panecho", "PanEcho", source="local")


def output(path):
    video = process_video(path)
    res = model(video)
    return humanize_result(res)
