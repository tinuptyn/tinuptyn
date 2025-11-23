/**
 * 实时天气交互式组件 - JavaScript模块
 * 可独立使用或集成到任何Web应用中
 * 
 * 使用方法:
 * const widget = new WeatherWidget('weather-container', 'YOUR_API_KEY');
 * widget.init('Beijing');
 */

class WeatherWidget {
    constructor(containerId, apiKey) {
        this.container = document.getElementById(containerId);
        this.apiKey = apiKey || 'YOUR_API_KEY_HERE';
        this.apiUrl = 'https://api.openweathermap.org/data/2.5/weather';
        this.isCelsius = true;
        this.currentData = null;
        
        this.weatherIcons = {
            '01d': '☀️', '01n': '🌙',
            '02d': '⛅', '02n': '☁️',
            '03d': '☁️', '03n': '☁️',
            '04d': '☁️', '04n': '☁️',
            '09d': '🌧️', '09n': '🌧️',
            '10d': '🌦️', '10n': '🌧️',
            '11d': '⛈️', '11n': '⛈️',
            '13d': '❄️', '13n': '❄️',
            '50d': '🌫️', '50n': '🌫️'
        };
    }

    // 初始化组件
    init(defaultCity = 'Beijing') {
        this.render();
        this.attachEventListeners();
        this.fetchWeather(defaultCity);
        this.startTimeUpdate();
        
        if (this.apiKey === 'YOUR_API_KEY_HERE') {
            console.warn('⚠️ 请设置OpenWeatherMap API密钥！');
            console.info('📝 注册地址: https://openweathermap.org/api');
        }
    }

    // 渲染组件HTML
    render() {
        this.container.innerHTML = `
            <style>
                .weather-widget {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 25px;
                    padding: 40px;
                    max-width: 450px;
                    width: 100%;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(10px);
                    animation: slideIn 0.5s ease-out;
                }

                @keyframes slideIn {
                    from { opacity: 0; transform: translateY(-30px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                .weather-search-box {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 30px;
                }

                .weather-search-input {
                    flex: 1;
                    padding: 12px 20px;
                    border: 2px solid #e0e0e0;
                    border-radius: 50px;
                    font-size: 16px;
                    outline: none;
                    transition: all 0.3s;
                }

                .weather-search-input:focus {
                    border-color: #667eea;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }

                .weather-btn {
                    padding: 12px 25px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 600;
                    transition: transform 0.2s, box-shadow 0.2s;
                }

                .weather-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }

                .weather-location-btn {
                    background: #f0f0f0;
                    border: none;
                    padding: 12px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 20px;
                    transition: all 0.3s;
                }

                .weather-location-btn:hover {
                    background: #e0e0e0;
                    transform: rotate(45deg);
                }

                .weather-info {
                    text-align: center;
                }

                .weather-city-name {
                    font-size: 32px;
                    font-weight: 700;
                    color: #333;
                    margin-bottom: 10px;
                }

                .weather-date-time {
                    font-size: 14px;
                    color: #666;
                    margin-bottom: 20px;
                }

                .weather-icon {
                    font-size: 100px;
                    margin: 20px 0;
                    animation: float 3s ease-in-out infinite;
                }

                @keyframes float {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }

                .weather-temperature {
                    font-size: 72px;
                    font-weight: 700;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin: 20px 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 10px;
                }

                .weather-unit-toggle {
                    font-size: 24px;
                    cursor: pointer;
                    background: #f0f0f0;
                    padding: 8px 15px;
                    border-radius: 20px;
                    transition: all 0.3s;
                }

                .weather-unit-toggle:hover {
                    background: #e0e0e0;
                }

                .weather-description {
                    font-size: 24px;
                    color: #555;
                    text-transform: capitalize;
                    margin-bottom: 30px;
                }

                .weather-details {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-top: 30px;
                }

                .weather-detail-item {
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 20px;
                    border-radius: 15px;
                    transition: transform 0.3s;
                }

                .weather-detail-item:hover {
                    transform: translateY(-5px);
                }

                .weather-detail-icon {
                    font-size: 28px;
                    margin-bottom: 8px;
                }

                .weather-detail-label {
                    font-size: 12px;
                    color: #666;
                    margin-bottom: 5px;
                }

                .weather-detail-value {
                    font-size: 18px;
                    font-weight: 600;
                    color: #333;
                }

                .weather-loading {
                    text-align: center;
                    color: #667eea;
                    font-size: 18px;
                    display: none;
                }

                .weather-loading.active {
                    display: block;
                }

                .weather-error {
                    background: #fee;
                    color: #c33;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    display: none;
                }

                .weather-error.active {
                    display: block;
                }

                @media (max-width: 480px) {
                    .weather-widget {
                        padding: 25px;
                    }
                    .weather-city-name {
                        font-size: 24px;
                    }
                    .weather-temperature {
                        font-size: 56px;
                    }
                    .weather-details {
                        grid-template-columns: 1fr;
                        gap: 15px;
                    }
                }
            </style>

            <div class="weather-widget">
                <div class="weather-search-box">
                    <input type="text" class="weather-search-input" id="weatherCityInput" placeholder="输入城市名称..." value="">
                    <button class="weather-location-btn" id="weatherLocationBtn" title="使用当前位置">📍</button>
                    <button class="weather-btn" id="weatherSearchBtn">搜索</button>
                </div>

                <div class="weather-error" id="weatherError"></div>
                <div class="weather-loading" id="weatherLoading">加载中...</div>

                <div class="weather-info" id="weatherInfo" style="display: none;">
                    <h1 class="weather-city-name" id="weatherCityName">--</h1>
                    <div class="weather-date-time" id="weatherDateTime">--</div>
                    
                    <div class="weather-icon" id="weatherIcon">🌤️</div>
                    
                    <div class="weather-temperature">
                        <span id="weatherTemp">--</span>
                        <span class="weather-unit-toggle" id="weatherUnitToggle" title="点击切换单位">°C</span>
                    </div>
                    
                    <div class="weather-description" id="weatherDescription">--</div>

                    <div class="weather-details">
                        <div class="weather-detail-item">
                            <div class="weather-detail-icon">💧</div>
                            <div class="weather-detail-label">湿度</div>
                            <div class="weather-detail-value" id="weatherHumidity">--%</div>
                        </div>
                        <div class="weather-detail-item">
                            <div class="weather-detail-icon">💨</div>
                            <div class="weather-detail-label">风速</div>
                            <div class="weather-detail-value" id="weatherWindSpeed">-- m/s</div>
                        </div>
                        <div class="weather-detail-item">
                            <div class="weather-detail-icon">🌡️</div>
                            <div class="weather-detail-label">体感温度</div>
                            <div class="weather-detail-value" id="weatherFeelsLike">--°</div>
                        </div>
                        <div class="weather-detail-item">
                            <div class="weather-detail-icon">👁️</div>
                            <div class="weather-detail-label">能见度</div>
                            <div class="weather-detail-value" id="weatherVisibility">-- km</div>
                        </div>
                        <div class="weather-detail-item">
                            <div class="weather-detail-icon">🔽</div>
                            <div class="weather-detail-label">气压</div>
                            <div class="weather-detail-value" id="weatherPressure">-- hPa</div>
                        </div>
                        <div class="weather-detail-item">
                            <div class="weather-detail-icon">☁️</div>
                            <div class="weather-detail-label">云量</div>
                            <div class="weather-detail-value" id="weatherClouds">--%</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // 绑定事件监听
    attachEventListeners() {
        const searchBtn = document.getElementById('weatherSearchBtn');
        const cityInput = document.getElementById('weatherCityInput');
        const locationBtn = document.getElementById('weatherLocationBtn');
        const unitToggle = document.getElementById('weatherUnitToggle');

        searchBtn.addEventListener('click', () => {
            const city = cityInput.value.trim();
            if (city) {
                this.fetchWeather(city);
            } else {
                this.showError('请输入城市名称');
            }
        });

        cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchBtn.click();
            }
        });

        locationBtn.addEventListener('click', () => {
            this.getUserLocation();
        });

        unitToggle.addEventListener('click', () => {
            this.toggleUnit();
        });
    }

    // 显示错误信息
    showError(message) {
        const errorEl = document.getElementById('weatherError');
        errorEl.textContent = message;
        errorEl.classList.add('active');
        setTimeout(() => {
            errorEl.classList.remove('active');
        }, 5000);
    }

    // 显示加载状态
    setLoading(isLoading) {
        const loadingEl = document.getElementById('weatherLoading');
        const infoEl = document.getElementById('weatherInfo');
        
        if (isLoading) {
            loadingEl.classList.add('active');
            infoEl.style.display = 'none';
        } else {
            loadingEl.classList.remove('active');
        }
    }

    // 更新日期时间
    updateDateTime() {
        const now = new Date();
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit',
            weekday: 'long'
        };
        document.getElementById('weatherDateTime').textContent = 
            now.toLocaleDateString('zh-CN', options);
    }

    // 开始时间更新
    startTimeUpdate() {
        setInterval(() => {
            if (this.currentData) {
                this.updateDateTime();
            }
        }, 30000); // 每30秒更新一次
    }

    // 温度转换
    convertTemp(kelvin, toCelsius = true) {
        if (toCelsius) {
            return Math.round(kelvin - 273.15);
        } else {
            return Math.round((kelvin - 273.15) * 9/5 + 32);
        }
    }

    // 获取天气数据
    async fetchWeather(city) {
        try {
            this.setLoading(true);
            
            // 如果没有配置API密钥，使用模拟数据
            if (this.apiKey === 'YOUR_API_KEY_HERE') {
                const mockData = this.getMockData(city);
                this.currentData = mockData;
                this.displayWeather(mockData);
                this.setLoading(false);
                return;
            }
            
            const response = await fetch(
                `${this.apiUrl}?q=${city}&appid=${this.apiKey}&lang=zh_cn`
            );
            
            if (!response.ok) {
                throw new Error('城市未找到或网络错误');
            }
            
            const data = await response.json();
            this.currentData = data;
            this.displayWeather(data);
            this.setLoading(false);
        } catch (error) {
            this.setLoading(false);
            this.showError(error.message || '获取天气数据失败，请稍后重试');
        }
    }

    // 通过地理位置获取天气
    async fetchWeatherByLocation(lat, lon) {
        try {
            this.setLoading(true);
            
            if (this.apiKey === 'YOUR_API_KEY_HERE') {
                const mockData = this.getMockData('当前位置');
                this.currentData = mockData;
                this.displayWeather(mockData);
                this.setLoading(false);
                return;
            }
            
            const response = await fetch(
                `${this.apiUrl}?lat=${lat}&lon=${lon}&appid=${this.apiKey}&lang=zh_cn`
            );
            
            if (!response.ok) {
                throw new Error('获取位置天气失败');
            }
            
            const data = await response.json();
            this.currentData = data;
            this.displayWeather(data);
            this.setLoading(false);
        } catch (error) {
            this.setLoading(false);
            this.showError('获取位置天气失败');
        }
    }

    // 显示天气数据
    displayWeather(data) {
        document.getElementById('weatherCityName').textContent = data.name;
        this.updateDateTime();
        
        const iconCode = data.weather[0].icon;
        document.getElementById('weatherIcon').textContent = 
            this.weatherIcons[iconCode] || '🌤️';
        
        const temp = this.convertTemp(data.main.temp, this.isCelsius);
        document.getElementById('weatherTemp').textContent = temp;
        
        document.getElementById('weatherDescription').textContent = 
            data.weather[0].description;
        document.getElementById('weatherHumidity').textContent = 
            `${data.main.humidity}%`;
        document.getElementById('weatherWindSpeed').textContent = 
            `${data.wind.speed} m/s`;
        
        const feelsLike = this.convertTemp(data.main.feels_like, this.isCelsius);
        document.getElementById('weatherFeelsLike').textContent = `${feelsLike}°`;
        
        document.getElementById('weatherVisibility').textContent = 
            `${(data.visibility / 1000).toFixed(1)} km`;
        document.getElementById('weatherPressure').textContent = 
            `${data.main.pressure} hPa`;
        document.getElementById('weatherClouds').textContent = 
            `${data.clouds.all}%`;

        document.getElementById('weatherInfo').style.display = 'block';
    }

    // 切换温度单位
    toggleUnit() {
        if (!this.currentData) return;
        
        this.isCelsius = !this.isCelsius;
        document.getElementById('weatherUnitToggle').textContent = 
            this.isCelsius ? '°C' : '°F';
        
        const temp = this.convertTemp(this.currentData.main.temp, this.isCelsius);
        document.getElementById('weatherTemp').textContent = temp;
        
        const feelsLike = this.convertTemp(
            this.currentData.main.feels_like, 
            this.isCelsius
        );
        document.getElementById('weatherFeelsLike').textContent = `${feelsLike}°`;
    }

    // 获取用户位置
    getUserLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.fetchWeatherByLocation(
                        position.coords.latitude, 
                        position.coords.longitude
                    );
                },
                (error) => {
                    this.showError('无法获取您的位置，请手动输入城市');
                }
            );
        } else {
            this.showError('您的浏览器不支持地理定位');
        }
    }

    // 获取模拟数据（用于演示）
    getMockData(cityName) {
        return {
            name: cityName,
            weather: [{
                description: '晴朗',
                icon: '01d'
            }],
            main: {
                temp: 295.15, // 22°C in Kelvin
                feels_like: 294.15,
                humidity: 65,
                pressure: 1013
            },
            wind: {
                speed: 3.5
            },
            visibility: 10000,
            clouds: {
                all: 20
            }
        };
    }
}

// 导出为全局变量或ES模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherWidget;
} else if (typeof define === 'function' && define.amd) {
    define([], function() { return WeatherWidget; });
} else {
    window.WeatherWidget = WeatherWidget;
}
