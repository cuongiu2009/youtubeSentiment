# YouTube Comment Stance Analyzer

Một công cụ phân tích web sử dụng AI để xác định lập trường (đồng ý, phản đối, trung lập) của các bình luận trên YouTube so với nội dung chính của video.

## Tính năng chính

- **Phân tích Video Đa phương thức:** Tự động lấy nội dung video bằng cách ưu tiên transcript có sẵn hoặc dùng AI Speech-to-Text làm phương án dự phòng.
- **Tóm tắt Nội dung:** Sử dụng model AI để tóm tắt nội dung video, tạo ra một "khẳng định chính" (main claim) ngắn gọn.
- **Phân tích Lập trường Bình luận:** Dùng model Zero-Shot Classification để so sánh từng bình luận với khẳng định chính của video, phân loại chúng thành `AGREEMENT`, `DISAGREEMENT`, hoặc `NEUTRAL`.
- **Lưu trữ Kết quả:** Tự động lưu kết quả phân tích chi tiết và bản ghi phiên âm ra file để dễ dàng xem xét, đánh giá.
- **Giao diện Web đơn giản:** Cho phép người dùng dễ dàng nhập URL và xem kết quả.

---

## Luồng hoạt động (Workflow)

1.  **Input:** Người dùng nhập một URL video YouTube vào giao diện web.
2.  **Backend Xử lý:**
    a.  **Lấy Nội dung Video:**
        - **Ưu tiên 1:** Gọi YouTube API để tìm và tải bản ghi phụ đề (transcript) có sẵn.
        - **Dự phòng:** Nếu không có transcript, dùng `yt-dlp` để tải file audio (`.mp3`) của video.
    b.  **Tạo Transcript:**
        - Nếu dùng phương án dự phòng, file audio sẽ được đưa qua model Speech-to-Text (hiện tại là `facebook/wav2vec2-base-960h`) để tạo ra bản ghi văn bản.
    c.  **Tóm tắt:** Toàn bộ bản ghi văn bản được đưa qua model Tóm tắt (`sshleifer/distilbart-cnn-12-6`) để tạo ra một `video_claim` (khẳng định chính) ngắn gọn.
    d.  **Lấy Bình luận:** Gọi YouTube API để lấy về danh sách các bình luận.
    e.  **Phân tích Lập trường:** Dùng model Zero-Shot Classification (`facebook/bart-large-mnli`) để so sánh từng bình luận với `video_claim`.
    f.  **Lưu trữ:** Kết quả phân tích đầy đủ được lưu vào file `.json`, và bản ghi phiên âm được lưu vào file `.txt` trong thư mục `reports/`.
3.  **Output:** Kết quả được trả về cho giao diện web và hiển thị cho người dùng.

---

## Kiến trúc Công nghệ (Tech Stack)

- **Backend:**
  - **Ngôn ngữ:** Python 3.11+
  - **Framework:** FastAPI
  - **Quản lý môi trường:** Poetry
  - **Thư viện AI:** `transformers` (Hugging Face), `torch`
  - **Tải Audio:** `yt-dlp`
  - **Xử lý Audio:** `soundfile`
- **Frontend:**
  - HTML5, CSS3, JavaScript (Vanilla)
- **Model AI:**
  - **Speech-to-Text:** `facebook/wav2vec2-base-960h`
  - **Summarization:** `sshleifer/distilbart-cnn-12-6`
  - **Stance Analysis (Zero-Shot):** `facebook/bart-large-mnli`

---

## Hướng dẫn Cài đặt & Sử dụng

### Yêu cầu

- Python 3.11+
- Poetry
- Node.js và npm
- **FFmpeg:** Cần được cài đặt và thêm vào `PATH` của hệ thống. (Có thể cài bằng `winget install "FFmpeg (Gyan)"` trên Windows).

### Các bước cài đặt

1.  **Clone dự án:**
    ```bash
    git clone <your-repo-url>
    cd youtubeSentiment
    ```

2.  **Cấu hình Backend:**
    a.  Di chuyển vào thư mục backend: `cd backend`
    b.  Cài đặt các thư viện: `poetry install`
    c.  Tạo file `.env` trong thư mục `backend` và thêm API key của bạn:
        ```
        YOUTUBE_API_KEY=AIzaSy...your...key...
        ```
    d.  Tạo file `cookies.txt` (hướng dẫn ở mục "Known Issues"). Đặt file này vào `backend/src/api/`.

3.  **Chạy Backend:**
    ```bash
    poetry run uvicorn src.api.main:app --reload
    ```
    Server sẽ chạy tại `http://localhost:8000`.

4.  **Chạy Frontend (mở một terminal khác):**
    a.  Di chuyển vào thư mục frontend: `cd frontend`
    b.  Cài đặt (nếu cần): `npm install`
    c.  Chạy server frontend:
        ```bash
        npx serve src
        ```
    Server sẽ chạy tại `http://localhost:3000` (hoặc một port khác).

5.  **Sử dụng:** Mở trình duyệt và truy cập địa chỉ của server frontend.

---

## Kiến trúc & Tùy chỉnh (Dành cho Developer)

Kiến trúc backend được thiết kế theo dạng service-oriented để dễ dàng bảo trì và thay thế.

-   **`main.py`:** Đóng vai trò là lớp API, nhận request và điều phối các service.
-   **`youtube_service.py`:** Chịu trách nhiệm mọi tương tác với bên ngoài (YouTube API, tải audio bằng `yt-dlp`).
-   **`ai_service.py`:** Chứa toàn bộ logic về AI (phiên âm, tóm tắt, phân tích lập trường). Đây là nơi bạn sẽ chỉnh sửa nếu muốn thay đổi model.

### Làm thế nào để thay đổi Model AI?

1.  **Tìm model trên Hugging Face:** Truy cập [Hugging Face Hub](https://huggingface.co/models) và tìm model phù hợp với tác vụ bạn muốn thay đổi (ví dụ: `summarization`).
2.  **Cập nhật `ai_service.py`:**
    *   Mở file `backend/src/services/ai_service.py`.
    *   Trong hàm `__init__`, thay đổi giá trị `model` trong các lệnh `pipeline()`.
    *   **Ví dụ:** Để đổi model tóm tắt, hãy sửa dòng này:
        ```python
        self.summarizer_pipeline = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6", # <-- Thay thế tên model ở đây
            device=0 if torch.cuda.is_available() else -1
        )
        ```

### Thay đổi phương pháp Phiên âm (Transcription)

File `ai_service.py` chứa 2 phương pháp trong hàm `transcribe_audio_file`:

1.  **Xử lý theo Chunk (Mặc định):** Dùng `soundfile` để đọc file audio theo từng đoạn nhỏ. An toàn cho máy có RAM yếu. Đây là code đang được kích hoạt.
2.  **Xử lý toàn bộ file:** Nhanh hơn trên máy mạnh. Để sử dụng, hãy **comment lại toàn bộ khối code của METHOD 1** và **bỏ comment khối code của METHOD 2**.

---

## Thách thức & Giải pháp (Technical Notes)

-   **Xử lý đường dẫn (Path Handling):** Gặp nhiều khó khăn với đường dẫn tương đối trên môi trường Windows khi chạy qua `poetry` và `uvicorn`. Giải pháp cuối cùng là sử dụng đường dẫn tuyệt đối được viết cứng (hardcoded) cho `ffmpeg` và `cookies.txt` trong `youtube_service.py`. Đây là một điểm cần cải thiện trong tương lai bằng cách dùng biến môi trường hoặc file cấu hình.

-   **YouTube Transcript API:** API này liên tục trả về lỗi `401 Unauthorized`, cho thấy nó có thể yêu cầu xác thực OAuth 2.0. Do đó, chức năng này đã bị vô hiệu hóa để tập trung vào giải pháp `yt-dlp` ổn định hơn.

-   **Xử lý Audio & Bộ nhớ:** Model AI ban đầu gặp lỗi hết bộ nhớ (`OutOfMemoryError`) khi xử lý video dài. Giải pháp là đọc và xử lý file audio theo từng chunk nhỏ bằng thư viện `soundfile`, hy sinh một chút tốc độ để đổi lấy sự ổn định.

-   **Xác thực `yt-dlp`:** YouTube có cơ chế chống bot. Giải pháp là sử dụng cookie từ trình duyệt đã đăng nhập để xác thực các yêu cầu tải xuống.
