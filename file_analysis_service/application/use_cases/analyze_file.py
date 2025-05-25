from collections import Counter
import re

from file_analysis_service.domain.entities import AnalysisResult
from file_analysis_service.domain.repositories import AnalysisResultRepository
from file_analysis_service.domain.ports import FileStoragePort, WordCloudPort
from file_analysis_service.application.dto import AnalyzeFileRequest, AnalyzeFileResponse


class AnalyzeFileUseCase:
    def __init__(
        self,
        repo: AnalysisResultRepository,
        storage: FileStoragePort,
        wordcloud: WordCloudPort,
        local_storage,  # инстанс LocalStorage
    ):
        self.repo = repo
        self.storage = storage
        self.wordcloud = wordcloud
        self.local_storage = local_storage

    def execute(self, req: AnalyzeFileRequest) -> AnalyzeFileResponse:
        # Если уже делали анализ – вернём прошлый
        existing = self.repo.get(req.file_id)
        if existing:
            return AnalyzeFileResponse(
                file_id=req.file_id,
                existing=True,
                word_count=existing.word_count,
                paragraph_count=existing.paragraph_count,
                top_chars=existing.top_chars,
            )

        # Загрузить файл
        content = self.storage.get_file(req.file_id)
        text = content.decode('utf-8', errors='ignore')

        # Подсчёт слов
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)

        # Подсчёт абзацев (разделяем по двойным переносам)
        paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
        paragraph_count = len(paragraphs)

        # Топ-10 символов (без пробелов)
        chars = [c for c in text.lower() if not c.isspace()]
        top_chars = [ch for ch, _ in Counter(chars).most_common(10)]

        # Генерация облака слов
        img = self.wordcloud.generate(text)
        # Сохранение картинки локально
        img_path = self.local_storage.store(f"{req.file_id}.png", img)

        # Сохранить в БД результаты
        result = AnalysisResult(
            file_id=req.file_id,
            word_count=word_count,
            paragraph_count=paragraph_count,
            top_chars=top_chars,
            image_location=img_path,
        )
        self.repo.save(result)

        return AnalyzeFileResponse(
            file_id=req.file_id,
            existing=False,
            word_count=word_count,
            paragraph_count=paragraph_count,
            top_chars=top_chars,
        )
