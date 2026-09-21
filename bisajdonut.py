import os
import time
import math


def main():
    # Terminal dimensions
    screen_width = 80
    screen_height = 24

    # Donut size
    R1 = 0.7   # Tube radius
    R2 = 1.5   # Distance from center

    # Camera / projection
    K1 = 28
    K2 = 5

    # Rotation angles
    A = 0.0
    B = 0.0

    # Characters from dark to bright
    illumination = ".,-~:;=!*#$@"

    # Clear screen once
    os.system("cls" if os.name == "nt" else "clear")

    try:
        while True:
            output = [" "] * (screen_width * screen_height)
            zbuffer = [0.0] * (screen_width * screen_height)

            # Pre-calculate rotation values
            cos_A = math.cos(A)
            sin_A = math.sin(A)
            cos_B = math.cos(B)
            sin_B = math.sin(B)

            theta = 0.0

            while theta < 2 * math.pi:
                cos_theta = math.cos(theta)
                sin_theta = math.sin(theta)

                phi = 0.0

                while phi < 2 * math.pi:
                    cos_phi = math.cos(phi)
                    sin_phi = math.sin(phi)

                    # Torus coordinates
                    circle_x = R2 + R1 * cos_theta
                    circle_y = R1 * sin_theta

                    # 3D rotation
                    x = (
                        circle_x * (
                            cos_B * cos_phi
                            + sin_A * sin_B * sin_phi
                        )
                        - circle_y * cos_A * sin_B
                    )

                    y = (
                        circle_x * (
                            sin_B * cos_phi
                            - sin_A * cos_B * sin_phi
                        )
                        + circle_y * cos_A * cos_B
                    )

                    z = (
                        K2
                        + cos_A * circle_x * sin_phi
                        + circle_y * sin_A
                    )

                    # Perspective
                    ooz = 1.0 / z

                    # Center the donut
                    xp = int(
                        screen_width / 2
                        + K1 * ooz * x * 2
                    )

                    yp = int(
                        screen_height / 2
                        - K1 * ooz * y
                    )

                    # Lighting
                    luminance = (
                        cos_phi * cos_theta * sin_B
                        - cos_A * cos_theta * sin_phi
                        - sin_A * sin_theta
                        + cos_B * (
                            cos_A * sin_theta
                            - cos_theta * sin_A * sin_phi
                        )
                    )

                    if luminance > 0:
                        if (
                            0 <= xp < screen_width
                            and 0 <= yp < screen_height
                        ):
                            position = xp + yp * screen_width

                            if ooz > zbuffer[position]:
                                zbuffer[position] = ooz

                                index = int(luminance * 8)

                                if index >= len(illumination):
                                    index = len(illumination) - 1

                                output[position] = illumination[index]

                    phi += 0.02

                theta += 0.07

            # Move cursor to top-left
            print("\033[H", end="")

            # Draw frame
            for y in range(screen_height):
                start = y * screen_width
                end = start + screen_width
                print("".join(output[start:end]))

            # Rotate
            A += 0.04
            B += 0.02

            # Frame rate
            time.sleep(0.03)

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
