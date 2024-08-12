// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const keywordContainer = document.querySelector('.keywords');
    const imageCardContainer = document.getElementById('image-card-container');
    const loadMoreBtn = document.getElementById('load-more-btn');

    let images = [];
    let keywords = [];
    let currentKeyword = 'all';
    let currentPage = 0;
    const itemsPerPage = 20;

    // 加载JSON文件
    fetch('data/images.json')
        .then(response => response.json())
        .then(data => {
            images = data;
            displayImages(images);
        });

    fetch('data/key.json')
        .then(response => response.json())
        .then(data => {
            keywords = ['最新', '全部', ...data.keywords];
            displayKeywords(keywords);
        });

    // 显示关键词按钮
    function displayKeywords(keywords) {
        keywords.forEach(keyword => {
            const button = document.createElement('button');
            button.classList.add('keyword-btn');
            button.textContent = keyword;
            button.dataset.keyword = keyword;
            if (keyword === '全部') {
                button.classList.add('selected');
            }
            keywordContainer.appendChild(button);
        });
    }

    // 显示图片卡片
    function displayImages(images) {
        const start = currentPage * itemsPerPage;
        const end = start + itemsPerPage;
        const pageImages = images.slice(start, end);

        pageImages.forEach(image => {
            const card = document.createElement('div');
            card.classList.add('image-card');
            card.innerHTML = `
                <img src="pic/${image.picPath}" alt="${image.title}">
                <div class="info">
                    <h3>${image.title}</h3>
                    <p>${image.tags.join(', ')}</p>
                    <p>${image.desc}</p>
                    <button class="detail-btn" data-url="${image.urlLink}">详情</button>
                </div>
            `;
            card.addEventListener('click', () => {
                window.open(image.urlLink, '_blank');
            });
            imageCardContainer.appendChild(card);
        });

        if (end < images.length) {
            loadMoreBtn.style.display = 'block';
        } else {
            loadMoreBtn.style.display = 'none';
        }
    }

    // 搜索功能
    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.toLowerCase();
        search(query); // 调用搜索函数并保存历史
        const filteredImages = images.filter(image => 
            image.title.toLowerCase().includes(query) ||
            image.desc.toLowerCase().includes(query) ||
            image.tags.some(tag => tag.toLowerCase().includes(query))
        );
        imageCardContainer.innerHTML = '';
        currentPage = 0;
        displayImages(filteredImages);
                    // 移除之前选中的关键词
                    document.querySelectorAll('.keyword-btn').forEach(btn => btn.classList.remove('selected'));
    });
    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') { 
            const query = searchInput.value.toLowerCase();
            search(query); // 调用搜索函数并保存历史
            const filteredImages = images.filter(image => 
                image.title.toLowerCase().includes(query) ||
                image.desc.toLowerCase().includes(query) ||
                image.tags.some(tag => tag.toLowerCase().includes(query))
            );
            imageCardContainer.innerHTML = '';
            currentPage = 0;
            displayImages(filteredImages);
                        // 移除之前选中的关键词
                        document.querySelectorAll('.keyword-btn').forEach(btn => btn.classList.remove('selected'));
        }
    });
    // 搜索历史
    function saveSearch(query) {
        let searchHistory = JSON.parse(localStorage.getItem('searchHistory')) || [];
        // 将新的搜索词添加到数组开始
        searchHistory.unshift(query);
        // 如果历史记录超过5条，移除最旧的记录
        if (searchHistory.length > 5) {
            searchHistory.pop();
        }
        // 更新本地存储
        localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
    }
    
    function getSearchHistory() {
        return JSON.parse(localStorage.getItem('searchHistory')) || [];
    }
    // 显示搜索历史
    function displaySearchHistory() {
        const searchHistory = getSearchHistory();
        const historyContainer = document.getElementById('searchHistory');
        historyContainer.innerHTML = ''; // 清空现有历史记录

        searchHistory.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.textContent = item;
            historyContainer.appendChild(historyItem);
        });
    }

    // 当鼠标悬停在搜索框上时，更新显示搜索历史
    searchInput.addEventListener('mouseover', displaySearchHistory);
    // 这里是搜索逻辑，包括保存搜索历史
    function search(query) {
        const filteredImages = images.filter(image => 
            image.title.toLowerCase().includes(query) ||
            image.desc.toLowerCase().includes(query) ||
            image.tags.some(tag => tag.toLowerCase().includes(query))
        );
        imageCardContainer.innerHTML = '';
        currentPage = 0;
        displayImages(filteredImages);
        saveSearch(query); // 保存搜索历史
    }

    // 关键词筛选功能
    keywordContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('keyword-btn')) {
            const keyword = event.target.dataset.keyword;
            let filteredImages = images;

            // 移除之前选中的关键词
            document.querySelectorAll('.keyword-btn').forEach(btn => btn.classList.remove('selected'));
            // 设置当前选中的关键词
            event.target.classList.add('selected');

            if (keyword === '最新') {
                filteredImages = images.sort((a, b) => new Date(b.refreshTime) - new Date(a.refreshTime));
            } else if (keyword === '全部') {
                filteredImages = images.sort((a, b) => b.hot - a.hot);
            } else {
                filteredImages = images.filter(image => image.tags.includes(keyword));
            }

            imageCardContainer.innerHTML = '';
            currentPage = 0;
            displayImages(filteredImages);
        }
    });

    // 加载更多功能
    loadMoreBtn.addEventListener('click', () => {
        currentPage++;
        displayImages(images);
    });
    // 新增：检测用户是否滚动到了页面底部的函数
    function isScrolledToBottom() {
        return (window.innerHeight + window.scrollY) >= document.body.offsetHeight;
    }

    // 处理滚动事件的函数
    function handleScroll() {
        if (isScrolledToBottom()) {
            currentPage++;
            displayImages(images);
        }
    }

    // 添加滚动事件监听器
    window.addEventListener('scroll', handleScroll);

    // 如果你仍然想保留点击按钮加载更多的功能，可以保留下面的代码
    loadMoreBtn.addEventListener('click', () => {
        currentPage++;
        displayImages(images);
    });
});