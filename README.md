# FIR Image Action Dataset

## Sensors

* Melexis *MLX90640-BAA* (short for mlx90640)
* Heimann *HTPA 32x32d L2.1* (short for htpa32)
* Raspberry Pi *Camera Module v2* (short for camerav2)

## Condition

| Description/Sensors      | mlx90640                  | htpa32-01                  | htpa32-02                  | camerav2                        |
| ------------------------ | ------------------------- | -------------------------- | -------------------------- | ------------------------------- |
| Sensor model             | Melexis *MLX90640-BAA*    | Heimann *HTPA 32x32d L2.1* | Heimann *HTPA 32x32d L2.1* | Raspberry Pi *Camera Module v2* |
| Resolution of the sensor | 32 × 24 pixels            | 32 × 32 pixels             | 32 × 32 pixels             | 320 × 240 pixels                |
| Sensor position          | Mid-center of the ceiling | Mid-center of the ceiling  | Corner of the ceiling      | Mid-center of the ceiling       |
| Sensor height            | 2355 mm                 |                            |                            |                                 |
| Sensor FOV               | 110° × 75°                | 90° × 90°                  | 90° × 90°                  | 62.2° × 48.8°                   |
| Viewing Direction        | Vertically downward       | Vertically downward        |                            | Vertically downward             |
| Frame rate               | 8 fps                     |                            |                            | 24fps                           |

## Dataset

### Environment

* At most one person in the room
* To get closer to the real environment, there is at least one heat source in the room.
* Two or three persons are acting in a sequence (No frames contain more than two persons at the same time.)

### Indoor scenes

### Actions

* "sit"
* "stand"
* "walk"
* "fall"
* "lie"
* "standup"
* "sitdown"
* "lying"

### Dataset file format

The data file name format as following:

`<date>_<sensor model>_<indoor scene>_<lighting>_<heat source>.csv`

E.g., 20200623_mlx90640_01_natural_none.csv

#### Sensor model

It's correspond to the sensors in the "Condition" part above, such as "mlx90640", "htpa32-01", "camerav2".

#### Lighting

* "light" means that data is collected when fluorescent lamp is turned on.
* "dark" means that data is collected at night without any light source.
* "natural" means that data is collected with natural lighting.

#### Heat source

There are five type of heat source.

* "none": no any heat source.

## Citations
```
@misc{zhang2020fir,
  title={FIR-Image-Action-Dataset},
  author={Zhang, H},
  year={2020},
  publisher={Rep{\'e}r{\'e} {\`a} https://github. com/visiongo-kr/FIR-Image-Action-Dataset\# fir-image~…}
}
```



