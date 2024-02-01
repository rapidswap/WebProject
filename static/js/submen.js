// JavaScript 코드
var menuLinks = document.querySelectorAll('.menu-link');
var openSubMenu = null; // 현재 열려있는 서브 메뉴를 저장할 변수

menuLinks.forEach(function(link) {
  link.addEventListener('click', function(event) {
    event.preventDefault(); // 기본 동작 막기

    var targetId = link.getAttribute('data-target');
    var subMenu = document.getElementById(targetId);

    // 이전에 열려있던 서브 메뉴가 있다면 닫기
    if (openSubMenu && openSubMenu !== subMenu) {
      openSubMenu.style.display = 'none'; // display: none으로 숨기기
    }

    // 서브 메뉴 항목들을 동적으로 배치하며 수평 레이아웃 유지
    if (subMenu.style.display === 'none') {
      subMenu.style.display = 'flex'; // display: flex로 나타내기
      subMenu.style.gap = '20px';
      openSubMenu = subMenu; // 현재 열려있는 서브 메뉴 저장
    } else {
      subMenu.style.display = 'none'; // display: none으로 숨기기
      openSubMenu = null; // 열려있는 서브 메뉴 초기화
    }
  });
});


function redirectToObjectives(event) {
  // 클릭된 요소의 href 값을 가져와서 이동 처리
  var hrefValue = event.currentTarget.getAttribute('href');

  // JavaScript로 페이지 이동 처리
  window.location.href = hrefValue;
}