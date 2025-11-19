import cv2
import sys

def scan_webcam(camera_index=0):
    # Use DirectShow (fixes MSMF camera errors on Windows)
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    # Optional: Set a safe resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Failed to read frame from webcam")
            break

        # Detect and decode QR
        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None:
            bbox = bbox.astype(int)

            # Draw bounding box
            for i in range(len(bbox)):
                pt1 = tuple(bbox[i][0])
                pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            if data:
                print("📌 QR Code detected:", data)
                cv2.putText(frame, data, (bbox[0][0][0], bbox[0][0][1] - 10),
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
        bbox = bbox.astype(int)

        # Draw bounding box
        for i in range(len(bbox)):
            pt1 = tuple(bbox[i][0])
            pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
            cv2.line(img, pt1, pt2, (0, 255, 0), 2)

    if data:
        print("📌 QR Code in image:", data)
        cv2.putText(img, data, (bbox[0][0][0], bbox[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        print("❌ No QR code found in image.")

    cv2.imshow("QR Scan - Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        scan_image(sys.argv[1])   # Run: python qr_scanner.py myqr.png
    else:
        scan_webcam()             # Run without arguments → Webcam Mode
