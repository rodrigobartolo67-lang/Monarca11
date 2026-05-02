import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import multer from 'multer';
import fs from 'node:fs/promises';
import path from 'node:path';

const app = express();
const PORT = process.env.PORT || 3000;
const uploadDir = path.join(process.cwd(), 'uploads');

await fs.mkdir(uploadDir, { recursive: true });

app.use(cors());
app.use(express.json({ limit: '2mb' }));
app.use(express.static(path.join(process.cwd(), 'public')));

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => cb(null, uploadDir),
  filename: (_req, file, cb) => {
    const timestamp = Date.now();
    const safeName = file.originalname.replace(/\s+/g, '_');
    cb(null, `${timestamp}-${safeName}`);
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: 1024 * 1024 * 1024 // 1GB
  }
});

app.post('/api/translate', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'Debes adjuntar un archivo.' });
    }

    const { sourceLanguage = 'auto', targetLanguage = 'es' } = req.body;

    const rawText = await fs.readFile(req.file.path, 'utf8');

    if (!rawText.trim()) {
      return res.status(400).json({ error: 'El archivo está vacío.' });
    }

    // Demo translator: replace this section with your preferred provider API.
    // In producción, conecta DeepL, Azure Translator, Google Cloud Translation o un motor local.
    const translatedText = `=== Traducción simulada (${sourceLanguage} -> ${targetLanguage}) ===\n\n${rawText}`;

    return res.json({
      fileName: req.file.originalname,
      sourceLanguage,
      targetLanguage,
      translatedText
    });
  } catch (error) {
    return res.status(500).json({ error: 'No se pudo procesar la traducción.', detail: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor activo en http://localhost:${PORT}`);
});
