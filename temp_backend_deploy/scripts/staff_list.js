function getShopList(count, offset){
	apiUrl = "https://api.staff-start.com/v2/shops/?merchant_id=2aab9b0c4ba0e94ad2f011fa10327b76&count=" + count;
	if(offset){
		apiUrl += "&offset=" + offset;
	}
	$.getJSON(apiUrl, function (json) {
		for(let i = 0; i < json.item.length; i++) {
			let option =  $('<option>', {value:json.item[i].shop_id}).text(json.item[i].name);
			$('#shopList').append(option);
		}
		let shop = getParam('shop');
		if(shop){
		  $('#shopList option[value=' + shop + ']').prop('selected', true);
		}
		if(count + offset < json.total){
			offset += count;
			getShopList(count, offset);
		}
	});
}
$(function () {
  // 店舗一覧取得
  getShopList(120, 0);
  
  // 絞り込み項目整理
  keyword = getParam('keyword');
  if(keyword){
	$('[name="keyword"]').val(keyword);
  }
  gender = getParam('gender');
  if(gender){
    $('[name=gender][value=' + gender + ']').prop('checked', true);
  } else {
	$('#gender0').prop('checked', true);
  }
  face = getParam('profile1');
  if(face){
    $('[name=profile1][value=' + face + ']').prop('checked', true);
    if(face == 'all'){
      face = "maru,sankaku,base,omonaga,tamago";
    }
  }
  sort = getParam('sort');
  if(sort){
    $('[name="sort"]').val(sort);
  } else {
	sort = "";
  }
  $('.staffListArchiveTab__item[data-sort="' + sort + '"]').addClass("staffListArchiveTab__item--active");
  
  // スタッフ一覧取得
  apiUrl = "https://api.staff-start.com/v1/staff/list/?merchant_id=2aab9b0c4ba0e94ad2f011fa10327b76";
  if(keyword){
	apiUrl += "&user_name=" + keyword;
  }
  if(gender){
    apiUrl += "&gender=" + gender;
  }
  if(face){
    apiUrl += "&user_attributes[][slug]=profile1&user_attributes[][value]=" + face;
  }
  shop = getParam('shop');
  if(shop){
    apiUrl += "&shop_id=" + shop;
  }
  if(sort){
    apiUrl += "&sort=" + sort;
  }
  page = getParam('page');
  if(page){
  	apiUrl += "&offset=" + (page - 1)*30;
  } else {
  	page = 1;
  }
  $.getJSON(apiUrl, function (json) {
	$('#seachNum').text(json.total);
	for(let i = 0; i < json.item.length; i++) {
		let card = $('<div>', {class: 'staffListArchive__item'});
		let cardHead = $('<a>', {class: 'staffListArchiveItem__header', href:"/shop/contents/staff_list_detail.aspx?staff_id=" + json.item[i].user_id });
		let col = $('<div>', {class: 'staff'});
		let colHead = $('<div>', {class: 'staff__header'});
		let thum = $('<div>', {class: 'staff__thum'});
		$('<img>', {src: getUserImage(json.item[i].resized_images, "s")}).appendTo(thum);
		colHead.append(thum);
		col.append(colHead);
		let colBody = $('<div>', {class: 'staff__body'});
		$('<p>', {class: 'staff__name'}).text(json.item[i].name).appendTo(colBody);
		let pd1 = $('<p>', {class: 'staff__data'});
		$('<span>').text(getUserAttribute(json.item[i].user_attributes, "profile1")).appendTo(pd1);
		$('<span>').text(getUserAttribute(json.item[i].user_attributes, "profile3")).appendTo(pd1);
		pd1.appendTo(colBody);
		let pd2 = $('<p>', {class: 'staff__data'});
		$('<span>').text(getUserAttribute(json.item[i].user_attributes, "profile2")).appendTo(pd2);
		pd2.appendTo(colBody);
		$('<p>', {class: 'staff__shop'}).text(json.item[i].shop_name).appendTo(colBody);
		col.append(colBody);
		cardHead.append(col);
		card.append(cardHead);
	
		let cardBody = $('<div>', {class: 'staffListArchiveItem__body'});
		apiUrl ="https://api.staff-start.com/v1/coordinate/?merchant_id=2aab9b0c4ba0e94ad2f011fa10327b76&sort=time&count=3&user_id=" + json.item[i].user_id;
		$.getJSON(apiUrl, function (json2) {
			for(let j = 0; j < json2.item.length; j++) {
				let collection = $('<div>', {class: 'staffListArchiveItemCollection'});
				if(json2.item[j].has_video){
					let mark =  $('<div>', {class: 'staffListArchiveItemCollection__mark'});
					$('<span>', {class: 'staffListArchiveItemCollectionMark__icon'}).appendTo(mark);
					collection.append(mark);
				}
				let cHead = $('<a>', {class: 'staffListArchiveItemCollection__media', href:"/shop/contents/staff_gallery_detail.aspx?cid=" + json2.item[j].cid });
				$('<img>', {src: json2.item[j].attachments[0].image_url.l}).appendTo(cHead);
				collection.append(cHead);
				cardBody.append(collection);
			}
		});
		card.append(cardBody);
		$('.staffListArchive__grid').append(card);
	}
	let pagenation = createPagination(Number(page), Math.ceil(json.total / 30), 4, 'staffListArchive');
	if(pagenation){
		$('.staffListArchive__grid').after(pagenation);
	}
  });
  
  $('#search').change(function(){
	$(this).submit();
  });
  $('.staffListArchiveTab__item').click(function(){
	$('[name="sort"]').val($(this).data('sort'));
	$('#search').submit();
  });

  /*-----------------------------------------------

  アコーディオン

  -----------------------------------------------*/
  $(function () {
    $('.js-accordion__toggle').click(function () {
      $(this).toggleClass('js-accordion__toggle--active');
      $(this).next('.js-accordion__target').slideToggle();
    });
  });

  /*-----------------------------------------------

  絞り込み表示非表示

  -----------------------------------------------*/
  $(function () {
    $("#sortBtn").click(function () {
      $("#sortTarget").toggleClass("active");
    });
  });
});
