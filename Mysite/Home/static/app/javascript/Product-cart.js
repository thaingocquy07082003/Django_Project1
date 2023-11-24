const $options = document.querySelectorAll('.color-option .circle');

  let $activeOption = document.querySelector('.color-option .circle.active');

  let $activeImage = document.querySelector('.Laptop_image .active');

  const handleOptionClick = (event) => {

    $activeOption.classList.remove('active');

    $activeOption = event.target;

    $activeOption.classList.add('active');



    const optionColors = $activeOption.dataset.option;

    $activeImage.classList.remove('active');

    $activeImage = document.querySelector(`.Laptop_image .${optionColors}`);

    $activeImage.classList.add('active');

  };

  $options.forEach(($ele) => {

      $ele.addEventListener(

          'click',

          handleOptionClick,

      );

  });