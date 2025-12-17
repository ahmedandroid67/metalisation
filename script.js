// API Configuration - Will be set by Coolify environment
const API_URL = window.location.origin;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const uploadPlaceholder = document.getElementById('uploadPlaceholder');
const imagePreview = document.getElementById('imagePreview');
const imageInput = document.getElementById('imageInput');
const previewImage = document.getElementById('previewImage');
const removeImageBtn = document.getElementById('removeImageBtn');
const arabicNameInput = document.getElementById('arabicNameInput');
const includeTextCheckbox = document.getElementById('includeTextCheckbox');
const generateBtn = document.getElementById('generateBtn');
const loadingContainer = document.getElementById('loadingContainer');
const resultSection = document.getElementById('resultSection');
const resultImage = document.getElementById('resultImage');
const downloadBtn = document.getElementById('downloadBtn');
const newGenerationBtn = document.getElementById('newGenerationBtn');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const errorCloseBtn = document.getElementById('errorCloseBtn');
const toggleSampleBtn = document.getElementById('toggleSampleBtn');
const sampleContent = document.getElementById('sampleContent');
const sampleHeader = document.getElementById('sampleHeader');

// State
let selectedImage = null;
let generatedImageData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkButtonState();
});

function setupEventListeners() {
    // Sample section toggle
    sampleHeader.addEventListener('click', toggleSample);

    // Upload area click
    uploadPlaceholder.addEventListener('click', () => {
        imageInput.click();
    });

    // File input change
    imageInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Remove image
    removeImageBtn.addEventListener('click', removeImage);

    // Arabic name input
    arabicNameInput.addEventListener('input', checkButtonState);

    // Text toggle checkbox
    includeTextCheckbox.addEventListener('change', checkButtonState);

    // Generate button
    generateBtn.addEventListener('click', generatePortrait);

    // Download button
    downloadBtn.addEventListener('click', downloadImage);

    // New generation button
    newGenerationBtn.addEventListener('click', resetForm);

    // Error close
    errorCloseBtn.addEventListener('click', hideError);
}

// Sample Toggle
function toggleSample() {
    sampleContent.classList.toggle('collapsed');
    toggleSampleBtn.classList.toggle('collapsed');
}

// File Handling
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadPlaceholder.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadPlaceholder.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    uploadPlaceholder.classList.remove('drag-over');

    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processFile(file);
    } else {
        showError('يرجى اختيار ملف صورة صحيح (PNG, JPG, JPEG)');
    }
}

function processFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('يرجى اختيار ملف صورة صحيح');
        return;
    }

    // Validate file size (16MB)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('حجم الصورة كبير جداً. الحد الأقصى 16 ميجابايت');
        return;
    }

    selectedImage = file;

    // Preview the image
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadPlaceholder.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        checkButtonState();
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    selectedImage = null;
    imageInput.value = '';
    previewImage.src = '';
    uploadPlaceholder.classList.remove('hidden');
    imagePreview.classList.add('hidden');
    checkButtonState();
}

// Form Validation
function checkButtonState() {
    const hasImage = selectedImage !== null;
    const hasName = arabicNameInput.value.trim().length > 0;
    const includeText = includeTextCheckbox.checked;

    // If text is included, require both image and name
    // If text is not included, only require image
    if (includeText) {
        generateBtn.disabled = !(hasImage && hasName);
    } else {
        generateBtn.disabled = !hasImage;
    }
}

// Generate Portrait
async function generatePortrait() {
    const includeText = includeTextCheckbox.checked;

    if (!selectedImage) {
        showError('يرجى اختيار صورة');
        return;
    }

    if (includeText && !arabicNameInput.value.trim()) {
        showError('يرجى إدخال الاسم بالعربية');
        return;
    }

    // Show loading state
    generateBtn.style.display = 'none';
    loadingContainer.classList.remove('hidden');
    resultSection.classList.add('hidden');

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedImage);
        formData.append('arabicName', arabicNameInput.value.trim());
        formData.append('includeText', includeTextCheckbox.checked ? 'true' : 'false');

        // Call API
        const response = await fetch(`${API_URL}/api/generate`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Display generated image
            generatedImageData = data.image;
            resultImage.src = data.image;

            // Show result
            loadingContainer.classList.add('hidden');
            resultSection.classList.remove('hidden');

            // Scroll to result
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            // Handle error
            throw new Error(data.error || data.suggestion || 'فشل في إنشاء الصورة');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'حدث خطأ أثناء إنشاء الصورة. يرجى المحاولة مرة أخرى');
        loadingContainer.classList.add('hidden');
        generateBtn.style.display = 'block';
    }
}

// Download Image
function downloadImage() {
    if (!generatedImageData) {
        showError('لا توجد صورة للتحميل');
        return;
    }

    // Create download link
    const link = document.createElement('a');
    const arabicName = arabicNameInput.value.trim();
    link.href = generatedImageData;
    link.download = `portrait_${arabicName}_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Reset Form
function resetForm() {
    // Reset image
    removeImage();

    // Reset name
    arabicNameInput.value = '';

    // Reset state
    generatedImageData = null;

    // Hide result
    resultSection.classList.add('hidden');

    // Show generate button
    generateBtn.style.display = 'block';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Error Handling
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.classList.add('hidden');
}

// Utility: Check server health
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_URL}/api/health`);
        if (response.ok) {
            console.log('✅ Server is running');
            return true;
        }
    } catch (error) {
        console.warn('⚠️ Server is not running. Please start the Flask server.');
        return false;
    }
}

// Check server on load
checkServerHealth();
