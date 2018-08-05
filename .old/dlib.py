import cv2
# based on Dlib: https://github.com/davisking/dlib/blob/master/dlib/image_transforms/interpolation.h

def chip_details(chip_points, img_points, rows, cols):
    assert chip_points.shape[0] == img_points.shape[0]
    assert chip_points.shape[0] >= 2
    
    # Find the best similarity transform
    # using only rotations, scale changes, and translations
    tform = [cv2.estimateRigidTransform(chip_points[i], img_points[i], False) for i in range(chip_points.shape[0])]
    tform = np.stack([x for x in tform if x is not None])
    
    # Pick out scale and rotation parameters from transform matrices
    y = tform[:, 1, 0]
    x = tform[:, 0, 0]
    angle = np.arctan2(y, x)
    scale = np.sqrt(x**2 + y**2)
    
    
    return rect, angle

def get_face_chip_details(dets, size=200, padding=0.2):
    assert dets.shape[1] == 68
    assert padding >= 0 and size > 0
    
    # Average positions of face points 17-67
    mean_face_shape_x = [
        0.000213256, 0.0752622, 0.18113, 0.29077, 0.393397, 0.586856, 0.689483, 0.799124,
        0.904991, 0.98004, 0.490127, 0.490127, 0.490127, 0.490127, 0.36688, 0.426036,
        0.490127, 0.554217, 0.613373, 0.121737, 0.187122, 0.265825, 0.334606, 0.260918,
        0.182743, 0.645647, 0.714428, 0.793132, 0.858516, 0.79751, 0.719335, 0.254149,
        0.340985, 0.428858, 0.490127, 0.551395, 0.639268, 0.726104, 0.642159, 0.556721,
        0.490127, 0.423532, 0.338094, 0.290379, 0.428096, 0.490127, 0.552157, 0.689874,
        0.553364, 0.490127, 0.42689
    ]
    mean_face_shape_y = [
        0.106454, 0.038915, 0.0187482, 0.0344891, 0.0773906, 0.0773906, 0.0344891,
        0.0187482, 0.038915, 0.106454, 0.203352, 0.307009, 0.409805, 0.515625, 0.587326,
        0.609345, 0.628106, 0.609345, 0.587326, 0.216423, 0.178758, 0.179852, 0.231733,
        0.245099, 0.244077, 0.231733, 0.179852, 0.178758, 0.216423, 0.244077, 0.245099,
        0.780233, 0.745405, 0.727388, 0.742578, 0.727388, 0.745405, 0.780233, 0.864805,
        0.902192, 0.909281, 0.902192, 0.864805, 0.784792, 0.778746, 0.785343, 0.778746,
        0.784792, 0.824182, 0.831803, 0.824182
    ]
    mean_face_shape = np.stack((mean_face_shape_x, mean_face_shape_y), axis=1)

    assert mean_face_shape.shape[0] == 68-17

    from_points = size*(padding+mean_face_shape)/(2*padding+1)
    to_points = dets
    
    # Ignore the chin (0-16)
    # Ignore the lower lip (55-59 and 65-67)
    # Ignore the eyebrows (17-26)
    to_points = np.concatenate((to_points[:, 27:55, :], to_points[:, 60:65, :]), axis=1)
    from_points = np.broadcast_to(np.concatenate((from_points[10:38, :], from_points[43:48, :]), axis=0), to_points.shape)
    
    return chip_details(from_points, to_points, size, size)