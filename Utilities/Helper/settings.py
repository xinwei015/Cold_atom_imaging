def inintParams():
    global widget_params, instrument_params, imgData, Type_of_file , absimgData, m_path, absimgDatas
    widget_params = {
        "Image Display Setting": {
            "bkgStatus": False,
            "pfStatus": False,
            "magStatus": True,
            "imgSource": "disk",  # default is disk, once click the start experiment button, then change to camera
            "mode": 0,  # 0 is video mode; 2 is hardware mode
            "pfMin": 0,
            "pfMax": 1000,
            "img_stack_num": 4,
            "absimg_stack_num": 3
        },
        'calculate Setting':{'mode':0,},
        'Fitting Setting': {'mode': 0},

        "Analyse Data Setting": {
            "autoStatus": False,
            "roiStatus": False,
            "add_cross_axes": False,
            # "add_ten": False,
            "AbsTrigerStatus": False,
            "magValue": 5.1,
            "ToPwr": 110,
            "Detu": 6,
            "Dia": 14,
            "Prefix":'Data',
        },
        "Miscellanea": {
            "MagStatus": False,
            "MagFactor": 1,
            "tmpfactor": 1,
            "GSFittingStatue": False,
            "NCountStatus": False,
            "NCountsfitting": False,
            "MotionRPStatus": False,
            "MOTBeamOD": 0,
            "MOTDetuning": 0,
            "MotPower": 0,
        }
    }
    instrument_params = {
        "Camera": {
            "index": None,
            "exposure time": 20,
            "shutter time": 20,
            "gain value": 1,
        },
        "SLM": {
            "slm model": "LCSLM",
        }
    }
    imgData = {
        "BkgImg": [],  # contain the background image data when load from disk
        "Img_data":[],
        "Img_photon_range": [],
        "WI": [],
        "WO": [],
        # "ROI_size": [0,0]
        }
    Img1 = []
    Img2 = []
    Img3 = []
    Img4 = []
    absimgData = [Img1,Img2,Img3,Img4]

    Img1s = []
    Img2s = []
    Img3s = []
    Img4s = []
    absimgDatas = [Img1s, Img2s, Img3s, Img4s]

    m_path = []
    Type_of_file = 'png'

    print("Initialize parameters finished")

