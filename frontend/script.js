document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const generateBtn = document.getElementById('generateBtn');
    const imagePreview = document.getElementById('imagePreview');
    const previewSection = document.getElementById('preview');
    const loader = document.getElementById('loader');
    const resultsGrid = document.getElementById('results');

    let selectedFile = null;

    imageUpload.addEventListener('change', (event) => {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                previewSection.style.display = 'block';
            };
            reader.readAsDataURL(selectedFile);
        }
    });

    generateBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            alert('먼저 이미지를 선택해주세요.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        // UI 초기화
        resultsGrid.innerHTML = '';
        loader.style.display = 'block';

        try {
            // 백엔드 API URL
            const apiUrl = 'http://localhost:8000/generate-cartoon/';
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`서버 오류: ${response.statusText}`);
            }

            const data = await response.json();

            // 결과 이미지 표시
            if (data.image_urls && data.image_urls.length > 0) {
                data.image_urls.forEach(url => {
                    const img = document.createElement('img');
                    // 백엔드 서버의 주소를 포함한 전체 URL로 만듭니다.
                    img.src = `http://localhost:8000${url}`;
                    resultsGrid.appendChild(img);
                });
            } else {
                alert('이미지를 생성하지 못했습니다.');
            }

        } catch (error) {
            console.error('Error:', error);
            alert(`오류가 발생했습니다: ${error.message}`);
        } finally {
            loader.style.display = 'none';
        }
    });
});
