import cv2
import time
import numpy as np

while True: 


    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Camera not found")
        exit()

    start_time = time.time()
    detected_shapes = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 2000:
                approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                corners = len(approx)

                if corners == 3:
                    shape = "Triangle"
                elif corners == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    ratio = w / float(h)
                    if 0.9 <= ratio <= 1.1:
                        shape = "Square"
                    else:
                        shape = "Rectangle"
                elif corners > 6:
                    shape = "Circle"
                else:
                    shape = "Unknown"

                detected_shapes.add(shape)


                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(approx)
                cx, cy = x + w // 2, y + h // 2
                cv2.putText(frame, shape, (cx - 40, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (255, 0, 0), 2)


        remaining = int(30 - (time.time() - start_time))
        cv2.putText(frame, f"Scanning: {remaining}s",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2)

        cv2.imshow("Shape Detection", frame)

        if time.time() - start_time > 30:
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


    detected_shapes = list(detected_shapes)

    if len(detected_shapes) == 0:
        print(" No shapes detected")
        continue   

    print("\nDetected Shapes:")
    for i, shape in enumerate(detected_shapes):
        print(f"{i}: {shape}")

    try:
        choice = int(input("\n Which shape should I draw? Enter number: "))
    except:
        print("Invalid input")
        continue

    if choice < 0 or choice >= len(detected_shapes):
        print(" Invalid choice")
        continue

    selected_shape = detected_shapes[choice]
    print(" Selected:", selected_shape)

    triangle_img = cv2.imread("Triangle_image.png")
    square_img = cv2.imread("square_image.jpg")
    circle_img = cv2.imread("Circle_image.png")

    confirm_img = np.ones((500, 500, 3), dtype=np.uint8) * 255

    if selected_shape == "Triangle" and triangle_img is not None:
        confirm_img = triangle_img
    elif selected_shape == "Square" and square_img is not None:
        confirm_img = square_img
    elif selected_shape == "Circle" and circle_img is not None:
        confirm_img = circle_img

    confirm_img = cv2.resize(confirm_img, (500, 500))

    cv2.putText(confirm_img, f"Drawing: {selected_shape}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3)

    cv2.imshow("Drawing Confirmation", confirm_img)

    print("Now drawing:", selected_shape)

    print("\nPress R → Detect again | Press Q → Quit")

    while True:
        key = cv2.waitKey(0) & 0xFF

        if key == ord('r') or key == ord('R'):
            print(" Restarting detection...")
            cv2.destroyAllWindows()
            break   
        elif key == ord('q') or key == ord('Q'):
            print(" Exiting...")
            cv2.destroyAllWindows()
            exit()
