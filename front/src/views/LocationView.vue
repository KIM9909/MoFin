<template>
  <div class="page-container">
    <div class="search-section">
      <div class="search-card">
        <div class="search-header">
          <div class="header-icon">🏦</div>
          <h1>은행 위치 찾기</h1>
          <p class="subtitle">가까운 은행을 쉽고 빠르게 찾아보세요</p>
        </div>

        <div class="search-form">
          <div class="form-group">
            <label>지역 검색</label>
            <div class="input-wrapper">
              <span class="input-icon">🔍</span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="지역을 입력하세요 (예: 강남구)"
                class="search-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label>은행 선택</label>
            <div class="select-wrapper">
              <span class="input-icon">🏦</span>
              <select v-model="selectedBank" class="bank-select">
                <option value="" disabled selected>은행을 선택해주세요</option>
                <option v-for="bank in banks" :key="bank" :value="bank">
                  {{ bank }}
                </option>
              </select>
            </div>
          </div>

          <div class="button-group">
            <button @click="searchLocations" class="search-btn primary">
              <span class="btn-icon">🔍</span>
              은행 찾기
            </button>
            <button @click="findNearbyBanks" class="search-btn secondary">
              <span class="btn-icon">📍</span>
              내 주변 은행 찾기
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="map-section">
      <div id="map"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const banks = ref(["국민은행", "우리은행", "신한은행", "하나은행", "농협은행", "기업은행"]);
const searchQuery = ref("");
const selectedBank = ref("");

let map = null;
let markers = [];
let userMarker = null;

const userMarkerSVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="36" viewBox="0 0 24 36">
    <!-- 마커 외형 -->
    <path 
      d="M12 0C5.4 0 0 5.4 0 12c0 8.034 10.766 15.9 11.225 16.225a1.5 1.5 0 0 0 1.55 0C13.234 27.9 24 20.034 24 12 24 5.4 18.6 0 12 0z"
      fill="#FF4444"
      class="marker-background"
    />
    <!-- 내부 흰색 원 -->
    <circle cx="12" cy="12" r="5" fill="white"/>
    <!-- 중앙 빨간 점 -->
    <circle cx="12" cy="12" r="2.5" fill="#FF4444"/>
  </svg>
`;

function loadKakaoScript() {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.id = "kakao-map-script";
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=50b0f5c0401025ade857fcfea4043f73&libraries=services,clusterer&autoload=false`;
    script.async = true;

    script.onload = () => {
      window.kakao.maps.load(() => {
        resolve();
      });
    };
    script.onerror = reject;

    document.head.appendChild(script);
  });
}

function initializeMap() {
  const container = document.getElementById("map");
  const options = {
    center: new window.kakao.maps.LatLng(37.5665, 126.9780),
    level: 3,
  };

  map = new window.kakao.maps.Map(container, options);
}

function searchLocations() {
  if (!searchQuery.value || !selectedBank.value || !map) {
    alert("지역과 은행을 입력하세요.");
    return;
  }

  clearMarkers();

  const ps = new window.kakao.maps.services.Places();
  const query = `${searchQuery.value} ${selectedBank.value}`;

  ps.keywordSearch(query, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      result.forEach(location => {
        addMarker(location);
      });

      if (result.length > 0) {
        const bounds = new window.kakao.maps.LatLngBounds();
        markers.forEach(({ marker }) => {
          bounds.extend(marker.getPosition());
        });
        map.setBounds(bounds);
      }
    } else {
      alert("해당 지역에 은행 정보를 찾을 수 없습니다.");
    }
  });
}

function findNearbyBanks() {
  if (!map) {
    alert("지도를 초기화하는 중입니다. 잠시 후 다시 시도해주세요.");
    return;
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      position => {
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;
        const userPosition = new window.kakao.maps.LatLng(userLat, userLng);
        
        clearMarkers();

        // 사용자 정의 오버레이로 현재 위치 표시
        const content = document.createElement('div');
        content.innerHTML = userMarkerSVG;
        
        userMarker = new window.kakao.maps.CustomOverlay({
          map: map,
          position: userPosition,
          content: content,
          yAnchor: 0.5,
          xAnchor: 0.5
        });

        map.setCenter(userPosition);
        map.setLevel(4);

        const searchOptions = {
          location: userPosition,
          radius: 2000,
          sort: window.kakao.maps.services.SortBy.DISTANCE
        };

        const ps = new window.kakao.maps.services.Places();
        const searchBank = selectedBank.value || "은행";
        
        ps.keywordSearch(searchBank, (result, status) => {
          if (status === window.kakao.maps.services.Status.OK) {
            const bounds = new window.kakao.maps.LatLngBounds();
            bounds.extend(userPosition);
            
            result.forEach(location => {
              addMarker(location);
              bounds.extend(new window.kakao.maps.LatLng(location.y, location.x));
            });
            
            map.setBounds(bounds);
          } else {
            alert("주변 은행 정보를 찾을 수 없습니다.");
          }
        }, searchOptions);
      },
      error => {
        console.error("사용자 위치를 가져오는데 실패했습니다:", error);
        alert("위치 정보를 가져올 수 없습니다.");
      },
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 5000
      }
    );
  } else {
    alert("현재 브라우저에서 위치 정보를 사용할 수 없습니다.");
  }
}

function addMarker(location) {
  const position = new window.kakao.maps.LatLng(location.y, location.x)
  const marker = new window.kakao.maps.Marker({
    map: map,
    position: position
  })
  
  const infowindow = new window.kakao.maps.InfoWindow({
    content: `
      <div class="custom-infowindow">
        <h3>${location.place_name}</h3>
        <p>${location.address_name}</p>
      </div>
    `
  })
  
  window.kakao.maps.event.addListener(marker, 'click', function() {
    markers.forEach(({ infowindow: iw }) => iw.close())
    infowindow.open(map, marker)
  })
  
  markers.push({ marker, infowindow })
}

function clearMarkers() {
  markers.forEach(({ marker, infowindow }) => {
    marker.setMap(null)
    infowindow.close()
  })
  markers = []
  
  if (userMarker) {
    userMarker.setMap(null)
    userMarker = null
  }
}

onMounted(async () => {
  try {
    await loadKakaoScript()
    initializeMap()
  } catch (error) {
    console.error("카카오맵 스크립트를 로드하는 중 문제가 발생했습니다:", error);
  }
});
</script>

<style scoped>
.page-container {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: 100vh;
}

.search-section {
  width: 400px;
  flex-shrink: 0;
}

.search-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.search-card:hover {
  transform: translateY(-5px);
}

.search-header {
  background: linear-gradient(135deg, #5c9c5f 0%, #458748 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.header-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.search-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.subtitle {
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
}

.search-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1a202c;
}

.input-wrapper, .select-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

.search-input, .bank-select {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

.search-input:focus, .bank-select:focus {
  outline: none;
  border-color: #5c9c5f;
  box-shadow: 0 0 0 3px rgba(92, 156, 95, 0.2);
  background-color: white;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn.primary {
  background: linear-gradient(135deg, #5c9c5f 0%, #458748 100%);
  color: white;
}

.search-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 156, 95, 0.3);
}

.search-btn.secondary {
  background-color: #f1f5f9;
  color: #1a202c;
  border: 2px solid #e2e8f0;
}

.search-btn.secondary:hover {
  background-color: #e2e8f0;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 1.2rem;
}

.map-section {
  flex-grow: 1;
  min-width: 0;
}

#map {
  width: 100%;
  height: 700px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.custom-infowindow {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.custom-infowindow h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #1a202c;
}

.custom-infowindow p {
  margin: 0;
  font-size: 0.9rem;
  color: #4a5568;
}

@media (max-width: 1024px) {
  .page-container {
    flex-direction: column;
    padding: 1rem;
  }

  .search-section {
    width: 100%;
  }

  #map {
    height: 500px;
    margin-top: 1rem;
  }

  .search-header {
    padding: 1.5rem;
  }

  .search-form {
    padding: 1.5rem;
  }
}

@media (min-width: 1025px) {
  .search-card {
    position: sticky;
    top: 2rem;
  }
}

</style>