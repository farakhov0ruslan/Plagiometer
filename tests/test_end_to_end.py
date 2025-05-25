import os
import time
import uuid

import pytest
import requests

GATEWAY = os.getenv("GATEWAY_URL", "http://localhost:8000")


@pytest.fixture(scope="session", autouse=True)
def wait_for_services():
    """
    Ждём, пока Gateway и File Service не станут готовы.
    Gateway → /health
    File Service → POST /api/files/ с минимальным payload (ожидаем 200 или 400).
    """
    # Ждём Gateway
    for _ in range(20):
        try:
            resp = requests.get(
                f"{GATEWAY}/health",
                timeout=1,
                proxies={"http": None, "https": None}
            )
            if resp.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        pytest.skip("Gateway is not available")

    # Ждём File Service (через Gateway прокси)
    for _ in range(20):
        try:
            # пустой файл скорее всего даст 400, но значит сервис жив
            r = requests.post(
                f"{GATEWAY}/api/files/",
                files={"file": ("ping.txt", b"", "text/plain")},
                proxies={"http": None, "https": None},
                timeout=1
            )
            if r.status_code in (200, 400):
                return
        except Exception:
            pass
        time.sleep(1)
    pytest.skip("File Service is not available via Gateway")


def test_file_upload_and_download(tmp_path):
    # 1) Создаём временный текстовый файл
    content = b"hello world!" + uuid.uuid4().bytes
    file_path = tmp_path / "hello.txt"
    file_path.write_bytes(content)

    # 2) Загружаем его в File Service через Gateway
    with open(file_path, "rb") as f:
        files = {"file": ("hello.txt", f, "text/plain")}
        r = requests.post(f"{GATEWAY}/api/files/", files=files,
                          proxies={"http": None, "https": None}, )
    assert r.status_code == 200
    data = r.json()
    file_id = data["file_id"]
    assert not data["existing"]

    # 3) Скачиваем обратно и проверяем содержимое
    r2 = requests.get(f"{GATEWAY}/api/files/{file_id}", timeout=5,
                      proxies={"http": None, "https": None}, )
    assert r2.status_code == 200
    assert r2.content == content


def test_analysis_and_wordcloud():
    # 1) Загружаем файл для анализа
    text = b"foo bar\n\nbaz baz foo"
    files = {"file": ("test.txt", text, "text/plain")}
    r_upload = requests.post(f"{GATEWAY}/api/files/", files=files, proxies={"http": None, "https": None})
    file_id = r_upload.json()["file_id"]

    # 2) Запрашиваем анализ
    r1 = requests.get(f"{GATEWAY}/analysis/{file_id}", timeout=5,
                      proxies={"http": None, "https": None})
    assert r1.status_code == 200, r1.text
    stats = r1.json()
    # Проверяем базовые поля
    assert stats["file_id"] == file_id
    assert stats["word_count"] == 5  # foo, bar, baz, baz, foo
    assert stats["paragraph_count"] == 2
    assert isinstance(stats["top_chars"], list) and len(stats["top_chars"]) <= 10

    # 3) Запрашиваем облако слов
    r2 = requests.get(f"{GATEWAY}/analysis/wordcloud/{file_id}", stream=True, timeout=10,
                      proxies={"http": None, "https": None} )
    assert r2.status_code == 200
    # убедимся, что первые байты — сигнатура PNG
    sig = r2.raw.read(8)
    assert sig == b"\x89PNG\r\n\x1a\n"
