import cv2

def scan_webcam(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and decode
        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None:
            # Draw bounding box
            for i in range(len(bbox)):
                pt1 = tuple(map(int, bbox[i][0]))
                pt2 = tuple(map(int, bbox[(i + 1) % len(bbox)][0]))
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            if data:
                print("QR Code detected:", data)
                # Show decoded text on screen
                cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("QR Scanner - Press 'q' to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def scan_image(path):
    detector = cv2.QRCodeDetector()
    img = cv2.imread(path)
    if img is None:
        print("❌ Could not open image:", path)
        return
    data, bbox, _ = detector.detectAndDecode(img)
    if bbox is not None:
        for i in range(len(bbox)):
            pt1 = tuple(map(int, bbox[i][0]))
            pt2 = tuple(map(int, bbox[(i + 1) % len(bbox)][0]))
            cv2.line(img, pt1, pt2, (0, 255, 0), 2)
    if data:
        print("QR Code in image:", data)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        print("No QR code found in image.")
    cv2.imshow("QR Scan - Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        scan_image(sys.argv[1])   # run with image path: python qr_scanner.py myqr.png
    else:
        scan_webcam()             # run without args → webcam
