/**
 * imageAnalyser.js — On-device image classification using TF.js.
 * Falls back gracefully if model is not available.
 */

const MODEL_URL    = '/models/skin_classifier/model.json';
const CATEGORIES   = ['wound', 'rash', 'skin_infection', 'eye_condition', 'other'];
const CONFIDENCE_THRESHOLD = 0.60;
const MAX_UPLOAD_BYTES = 200 * 1024; // 200 KB

let _model = null;

/** Load the TF.js model (lazy). Returns null if unavailable. */
async function loadModel() {
  if (_model) return _model;
  try {
    // Dynamic import so the app doesn't crash if @tensorflow/tfjs isn't installed
    const tf = await import('@tensorflow/tfjs').catch(() => null);
    if (!tf) return null;
    _model = await tf.loadLayersModel(MODEL_URL);
    return _model;
  } catch {
    return null;
  }
}

/**
 * Analyse an image blob and return classification result.
 * @param {Blob} imageBlob
 * @returns {{ category: string, confidence: number, low_confidence: boolean }}
 */
export async function analyseImage(imageBlob) {
  const model = await loadModel();

  if (!model) {
    // Model not available — return 'other' with low confidence
    return { category: 'other', confidence: 0, low_confidence: true, model_unavailable: true };
  }

  try {
    const tf      = await import('@tensorflow/tfjs');
    const imgEl   = await blobToImageElement(imageBlob);
    const tensor  = tf.browser.fromPixels(imgEl).resizeBilinear([224, 224]).expandDims(0).div(255.0);
    const preds   = await model.predict(tensor).data();
    tensor.dispose();

    const maxIdx    = preds.indexOf(Math.max(...preds));
    const confidence = preds[maxIdx];
    const category   = CATEGORIES[maxIdx] || 'other';

    return {
      category,
      confidence: Math.round(confidence * 100) / 100,
      low_confidence: confidence < CONFIDENCE_THRESHOLD,
    };
  } catch {
    return { category: 'other', confidence: 0, low_confidence: true };
  }
}

/**
 * Compress an image blob to ≤200 KB.
 * @param {Blob} blob
 * @returns {Promise<Blob>}
 */
export async function compressImage(blob) {
  if (blob.size <= MAX_UPLOAD_BYTES) return blob;

  return new Promise((resolve) => {
    const img    = new Image();
    const objUrl = URL.createObjectURL(blob);
    img.onload = () => {
      URL.revokeObjectURL(objUrl);
      const canvas  = document.createElement('canvas');
      let { width, height } = img;
      const scale   = Math.sqrt(MAX_UPLOAD_BYTES / blob.size);
      canvas.width  = Math.floor(width * scale);
      canvas.height = Math.floor(height * scale);
      canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((compressed) => resolve(compressed || blob), 'image/jpeg', 0.7);
    };
    img.src = objUrl;
  });
}

/** Schedule auto-delete of an image record after 30 days. */
export function scheduleImageDelete(imageId) {
  const deleteAt = Date.now() + 30 * 24 * 60 * 60 * 1000;
  try {
    const schedule = JSON.parse(localStorage.getItem('ha_image_delete_schedule') || '{}');
    schedule[imageId] = deleteAt;
    localStorage.setItem('ha_image_delete_schedule', JSON.stringify(schedule));
  } catch { /* ignore */ }
}

/** Run pending image deletions. Call on app startup. */
export function runImageDeleteSchedule(deleteCallback) {
  try {
    const schedule = JSON.parse(localStorage.getItem('ha_image_delete_schedule') || '{}');
    const now      = Date.now();
    const updated  = {};
    for (const [id, deleteAt] of Object.entries(schedule)) {
      if (now >= deleteAt) {
        deleteCallback(id);
      } else {
        updated[id] = deleteAt;
      }
    }
    localStorage.setItem('ha_image_delete_schedule', JSON.stringify(updated));
  } catch { /* ignore */ }
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function blobToImageElement(blob) {
  return new Promise((resolve, reject) => {
    const img    = new Image();
    const objUrl = URL.createObjectURL(blob);
    img.onload  = () => { URL.revokeObjectURL(objUrl); resolve(img); };
    img.onerror = reject;
    img.src     = objUrl;
  });
}
