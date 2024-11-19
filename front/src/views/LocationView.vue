<template>
  <div class="container">
    <div class="form-container">
      <div class="form">
      <h1>은행 위치 찾기</h1>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="지역을 입력하세요 (예: 강남구)"
        />
        <select v-model="selectedBank">
          <option value="" disabled selected>은행 선택</option>
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
        <button @click="searchLocations">은행 찾기</button>
        <button @click="findNearbyBanks">내 주변 은행 찾기</button>
      </div>
    </div>
    <div id="map"></div>
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
        
        // 사용자 위치 마커 추가
        userMarker = new window.kakao.maps.Marker({
          map: map,
          position: userPosition,
          image: new window.kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new window.kakao.maps.Size(32, 35),  // 마커 크기를 32x35로 축소
            { offset: new window.kakao.maps.Point(16, 35) }  // 오프셋도 비율에 맞게 조정
          )
        });

        map.setCenter(userPosition);
        map.setLevel(4); // 줌 레벨 조정

        // 주변 은행 검색을 위한 옵션 설정
        const searchOptions = {
          location: userPosition,
          radius: 2000,  // 2km 반경
          sort: window.kakao.maps.services.SortBy.DISTANCE
        };

        const ps = new window.kakao.maps.services.Places();
        
        // 선택된 은행이 있으면 해당 은행만, 없으면 모든 은행 검색
        const searchBank = selectedBank.value || "은행";
        
        ps.keywordSearch(searchBank, (result, status) => {
          if (status === window.kakao.maps.services.Status.OK) {
            const bounds = new window.kakao.maps.LatLngBounds();
            bounds.extend(userPosition); // 사용자 위치를 범위에 포함
            
            result.forEach(location => {
              addMarker(location);
              bounds.extend(new window.kakao.maps.LatLng(location.y, location.x));
            });
            
            map.setBounds(bounds);
          } else {
            alert("주변 은행 정보를 찾을 수 없습니다.");
          }
        }, searchOptions); // 검색 옵션 적용
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
  const position = new window.kakao.maps.LatLng(location.y, location.x);
  const marker = new window.kakao.maps.Marker({
    map: map,
    position: position
  });
  
  const infowindow = new window.kakao.maps.InfoWindow({
    content: `
      <div style="padding:5px;font-size:12px;">
        <strong>${location.place_name}</strong><br/>
        ${location.address_name}
      </div>
    `
  });
  
  window.kakao.maps.event.addListener(marker, 'click', function() {
    markers.forEach(({ infowindow: iw }) => iw.close());
    infowindow.open(map, marker);
  });
  
  markers.push({ marker, infowindow });
}

function clearMarkers() {
  markers.forEach(({ marker, infowindow }) => {
    marker.setMap(null);
    infowindow.close();
  });
  markers = [];
  
  if (userMarker) {
    userMarker.setMap(null);
    userMarker = null;
  }
}

onMounted(async () => {
  try {
    await loadKakaoScript();
    initializeMap();
  } catch (error) {
    console.error("카카오맵 스크립트를 로드하는 중 문제가 발생했습니다:", error);
  }
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.form-container {
  width: 300px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding-top: 50px;
}

#map {
  flex-grow: 1;
  height: 550px;
  width: 500px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

input,
select,
button {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}
</style>