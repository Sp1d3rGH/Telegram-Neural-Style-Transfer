import numpy as np
import tensorflow as tf

from tensorflow.python.keras import models
from PIL import Image


def load_img(img_path):
    img = Image.open(img_path)
    img = tf.keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.vgg19.preprocess_input(img)
    return img


def undo_vgg19_preprocess(img_array):
    image_array = img_array.copy()

    if len(image_array.shape) == 4:
        image_array = np.squeeze(image_array, 0)

    image_array[:, :, 0] += 103.939
    image_array[:, :, 1] += 116.779
    image_array[:, :, 2] += 123.68
    image_array = image_array[:, :, ::-1]

    image_array = np.clip(image_array, 0, 255).astype('uint8')
    return image_array


def create_vgg19_model():
    vgg = tf.keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
    vgg.trainable = False

    style_outputs = [vgg.get_layer(name).output for name in style_layers]
    content_outputs = [vgg.get_layer(name).output for name in content_layers]
    model_outputs = style_outputs + content_outputs

    return models.Model(vgg.input, model_outputs)


def content_loss(base_content, target):
    return tf.reduce_mean(tf.square(base_content - target))


def gram_matrix(input_tensor):
    channels = int(input_tensor.shape[-1])
    a = tf.reshape(input_tensor, [-1, channels])
    n = tf.shape(a)[0]
    gram = tf.matmul(a, a, transpose_a=True)
    return gram / tf.cast(n, tf.float32)


def style_loss(base_style, gram_target):
    gram_style = gram_matrix(base_style)
    return tf.reduce_mean(tf.square(gram_style - gram_target))


def style_and_content_features(model, content_path, style_path):
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    style_outputs = model(style_image)
    content_outputs = model(content_image)

    style_features = [style_layer[0] for style_layer in style_outputs[:num_style_layers]]
    content_features = [content_layer[0] for content_layer in content_outputs[num_style_layers:]]

    return style_features, content_features


def compute_loss(model, loss_weights, init_image, gram_style_features, content_features):
    style_weight, content_weight = loss_weights

    model_outputs = model(init_image)

    style_output_features = model_outputs[:num_style_layers]
    content_output_features = model_outputs[num_style_layers:]

    style_score = 0
    content_score = 0

    weight_per_style_layer = 1.0 / float(num_style_layers)
    for target_style, comb_style in zip(gram_style_features, style_output_features):
        style_score += weight_per_style_layer * style_loss(comb_style[0], target_style)

    weight_per_content_layer = 1.0 / float(num_content_layers)
    for target_content, comb_content in zip(content_features, content_output_features):
        content_score += weight_per_content_layer * content_loss(comb_content[0], target_content)

    style_score *= style_weight
    content_score *= content_weight

    loss = style_score + content_score

    return loss, style_score, content_score


def compute_grads(cfg):
    with tf.GradientTape() as tape:
        all_loss = compute_loss(**cfg)

    total_loss = all_loss[0]
    return tape.gradient(total_loss, cfg['init_image']), all_loss


def run_style_transfer(content_path, style_path, num_iterations, content_weight=1e3, style_weight=1e-2):
    model = create_vgg19_model()
    for layer in model.layers:
        layer.trainable = False

    style_features, content_features = style_and_content_features(model, content_path, style_path)
    gram_style_features = [gram_matrix(style_feature) for style_feature in style_features]

    init_image = load_img(content_path)
    init_image = tf.Variable(init_image, dtype=tf.float32)
    opt = tf.optimizers.Adam(learning_rate=5, epsilon=1e-1)

    best_loss = float('inf')
    best_img = None

    loss_weights = (style_weight, content_weight)
    cfg = {'model': model, 'loss_weights': loss_weights, 'init_image': init_image, 'gram_style_features': gram_style_features, 'content_features': content_features}

    norm_means = np.array([103.939, 116.779, 123.68])
    min_vals = -norm_means
    max_vals = 255 - norm_means

    for i in range(num_iterations):
        grads, all_loss = compute_grads(cfg)
        loss, style_score, content_score = all_loss
        opt.apply_gradients([(grads, init_image)])
        clipped = tf.clip_by_value(init_image, min_vals, max_vals)
        init_image.assign(clipped)

        if loss < best_loss:
            best_loss = loss
            best_img = undo_vgg19_preprocess(init_image.numpy())

    return best_img


def start_nst(input_path, input_style_path, iterations, path_to_file):
    final_image = Image.fromarray(run_style_transfer(input_path, input_style_path, num_iterations=iterations))
    final_image.save(path_to_file)


content_layers = ['block5_conv2']
style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']

num_content_layers = len(content_layers)
num_style_layers = len(style_layers)