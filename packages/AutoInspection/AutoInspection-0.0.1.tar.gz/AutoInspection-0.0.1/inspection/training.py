import os
import cv2
import shutil
import json
import pathlib
import matplotlib.pyplot as plt
import keras
from keras import layers, models
from keras.models import Sequential
from datetime import datetime
from hexss import json_load, json_update
from hexss.constants import *
from hexss.image import controller, crop_img


def save_img(model_name, frame_dict):
    """Save cropped and processed images."""
    # Remove existing folders
    for path in [IMG_FRAME_LOG_PATH, IMG_FRAME_PATH]:
        folder = os.path.join(path, model_name)
        if os.path.exists(folder):
            shutil.rmtree(folder)

    # Get list of image files
    img_files = [f.split('.')[0] for f in os.listdir(IMG_FULL_PATH) if f.endswith(('.png', '.json'))]
    img_files = sorted(set(img_files), reverse=True)

    for i, file_name in enumerate(img_files):
        print(f'{i + 1}/{len(img_files)} {file_name}')

        frames = json_load(f"{IMG_FULL_PATH}/{file_name}.json")
        img = cv2.imread(f"{IMG_FULL_PATH}/{file_name}.png")

        for pos_name, status in frames.items():
            if pos_name not in frame_dict:
                print(f'{pos_name} not in frames')
                continue

            if frame_dict[pos_name]['model_used'] != model_name:
                continue

            print(f'    {model_name} {pos_name} {status}')

            xywh = frame_dict[pos_name]['xywh']

            # Save original cropped image
            img_crop = crop_img(img, xywh, resize=(180, 180))
            log_path = os.path.join(IMG_FRAME_LOG_PATH, model_name)
            os.makedirs(log_path, exist_ok=True)
            cv2.imwrite(f"{log_path}/{status} {pos_name} {file_name}.png", img_crop)

            # Process and save variations
            frame_path = os.path.join(IMG_FRAME_PATH, model_name, status)
            os.makedirs(frame_path, exist_ok=True)

            shift = [-4, -2, 0, 1, 4]
            # shift = [-4, 0, 4]
            for shift_y in shift:
                for shift_x in shift:
                    img_crop = crop_img(img, xywh, shift=(shift_x, shift_y), resize=(180, 180))

                    for brightness in [-24, -12, 0, 12, 24]:
                        for contrast in [-12, -6, 0, 6, 12]:
                            img_crop_BC = controller(img_crop, brightness, contrast)

                            output_filename = f"{file_name} {pos_name} {status} {shift_y} {shift_x} {brightness} {contrast}.png"
                            cv2.imwrite(os.path.join(frame_path, output_filename), img_crop_BC)


def create_model(model_name, img_height, img_width, batch_size, epochs):
    """Create and train a model."""
    data_dir = pathlib.Path(rf'{IMG_FRAME_PATH}/{model_name}')
    image_count = len(list(data_dir.glob('*/*.png')))
    print(f'image_count = {image_count}')

    train_ds, val_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="both",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    class_names = train_ds.class_names
    print('class_names =', class_names)

    with open(fr'{MODEL_PATH}/{model_name}.json', 'w') as file:
        file.write(json.dumps({"model_class_names": class_names}, indent=4))

    # Visualize the data
    plt.figure(figsize=(20, 10))
    for images, labels in train_ds.take(1):
        for i in range(32):
            ax = plt.subplot(4, 8, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")
    plt.savefig(f'{MODEL_PATH}/{model_name}.png')

    # Configure the dataset for performance
    AUTOTUNE = -1
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Create the model
    num_classes = len(class_names)
    model = Sequential([
        layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
        layers.Conv2D(16, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    model.summary()
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

    # Visualize training results
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)
    plt.figure(figsize=(10, 8))
    plt.plot(epochs_range, val_acc, label='Validation Accuracy', c=(0, 0.8, 0.5))
    plt.plot(epochs_range, acc, label='Training Accuracy', ls='--', c=(0, 0, 1))
    plt.plot(epochs_range, val_loss, label='Validation Loss', c=(1, 0.5, 0.1))
    plt.plot(epochs_range, loss, label='Training Loss', c='r', ls='--')
    plt.legend(loc='right')
    plt.title(model_name)
    plt.savefig(fr'{MODEL_PATH}/{model_name}_graf.png')

    model.save(os.path.join(MODEL_PATH, f'{model_name}.h5'))

    # Clean up
    shutil.rmtree(fr"{IMG_FRAME_PATH}/{model_name}")


def training_(inspection_name, config):
    global IMG_FULL_PATH, IMG_FRAME_PATH, IMG_FRAME_LOG_PATH, MODEL_PATH

    img_height = config['img_height']
    img_width = config['img_width']
    batch_size = config['batch_size']
    epochs = config['epochs']
    projects_directory = config['projects_directory']

    inspection_name_dir = os.path.join(projects_directory, f"auto_inspection_data__{inspection_name}")

    # Paths
    IMG_FULL_PATH = f'{inspection_name_dir}/img_full'
    IMG_FRAME_PATH = f'{inspection_name_dir}/img_frame'
    IMG_FRAME_LOG_PATH = f'{inspection_name_dir}/img_frame_log'
    MODEL_PATH = f'{inspection_name_dir}/model'

    # Create necessary directories
    for path in [IMG_FULL_PATH, IMG_FRAME_PATH, IMG_FRAME_LOG_PATH, MODEL_PATH]:
        os.makedirs(path, exist_ok=True)

    model_list = [file.split('.')[0] for file in os.listdir(MODEL_PATH) if file.endswith('.h5')]
    print()
    print(f'{CYAN}===========  {inspection_name}  ==========={END}')
    print(f'model.h5 (ที่มี) = {len(model_list)} {model_list}')

    json_data = json_load(os.path.join(inspection_name_dir, 'frames pos.json'))
    frame_dict = json_data['frames']
    model_dict = json_data['models']

    for model_name, model in model_dict.items():
        # อ่าน wait_training.json
        wait_training_dict = json_load(f'{inspection_name_dir}/wait_training.json', {})

        if not wait_training_dict.get(model_name, True):
            print(f'continue {model_name}')
            continue
        print()
        print(f'{model_name} {model}')
        t1 = datetime.now()
        print('-------- >>> crop_img <<< ---------')

        save_img(model_name, frame_dict)
        t2 = datetime.now()
        print(f'{t2 - t1} เวลาที่ใช้ในการเปลียน img_full เป็น shift_img ')
        print('------- >>> training... <<< ---------')
        create_model(model_name, img_height, img_width, batch_size, epochs)
        json_update(f'{inspection_name_dir}/wait_training.json', {model_name: False})
        t3 = datetime.now()
        print(f'{t2 - t1} เวลาที่ใช้ในการเปลียน img_full เป็น shift_img ')
        print(f'{t3 - t2} เวลาที่ใช้ในการ training ')
        print(f'{t3 - t1} เวลาที่ใช้ทั้งหมด')
        print()


def training(*args, config):
    for inspection_name in args:
        training_(inspection_name, config)


if __name__ == '__main__':
    training(
        "QC7-7990-000",
        "QD1-1988-000",
        "POWER-SUPPLY-FIXING-UNIT",
        "POWER-SUPPLY-FIXING-UNIT2",
        config={
            'projects_directory': 'C:\\PythonProjects\\',
            'batch_size': 32,
            'img_height': 180,
            'img_width': 180,
            'epochs': 5,
        }
    )
