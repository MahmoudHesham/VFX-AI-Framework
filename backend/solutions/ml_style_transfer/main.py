# This script copyrights belong to VFXKitchen. and the used solutions authors as mentioned.
# And it's available for academic and non-commercial use only.

# this solution is cloned from this repo
# https://github.com/lengstrom/fast-style-transfer
# and the copyrights belongs to it's authors as mentioned there

import sys
import tempfile
import numpy as np, os
import tensorflow as tf
from .style_transfer_utils import net, save_img, get_img

def fast_style_transfer(image_input_path, image_output_path, style, device_t='/gpu:0', batch_size=4):

    image_input_path = [image_input_path]
    image_output_path = [image_output_path]

    is_paths = type(image_input_path[0]) == str
    
    if is_paths:
        img_shape = get_img(image_input_path[0]).shape
    else:
        img_shape = X[0].shape

    g = tf.Graph()
    batch_size = min(len(image_output_path), batch_size)
    curr_num = 0
    soft_config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True
    
    with g.as_default(), g.device(device_t), tf.compat.v1.Session(config=soft_config) as sess:
        
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.compat.v1.placeholder(tf.float32, shape=batch_shape, name='img_placeholder')

        preds = net(img_placeholder)
        saver = tf.compat.v1.train.Saver()
        
        saver.restore(sess, style)
        num_iters = int(len(image_output_path)/batch_size)

        for i in range(num_iters):

            pos = i * batch_size
            curr_batch_out = image_output_path[pos:pos+batch_size]

            if is_paths:
                curr_batch_in = image_input_path[pos:pos+batch_size]
                X = np.zeros(batch_shape, dtype=np.float32)
                for j, path_in in enumerate(curr_batch_in):
                    img = get_img(path_in)
                    X[j] = img
            else:
                X = image_input_path[pos:pos+batch_size]

            _preds = sess.run(preds, feed_dict={img_placeholder:X})
            for j, path_out in enumerate(curr_batch_out):
                save_img(path_out, _preds[j])

        remaining_in = image_input_path[num_iters*batch_size:]
        remaining_out = image_output_path[num_iters*batch_size:]
    
    if len(remaining_in) > 0:
        fast_style_transfer(remaining_in, remaining_out, style, device_t=device_t, batch_size=1)

    print("Style transfer completed.")
    return image_output_path[0]