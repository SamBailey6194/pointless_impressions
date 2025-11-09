(()=>{function w(t){let e=document.getElementById("artwork-list");if(!e)return;let s=typeof getCloudinaryUrl<"u"&&typeof ARTWORK_DETAIL_BASE_PATH<"u",i=typeof ARTWORK_LIST_URL<"u"?ARTWORK_LIST_URL:"/artworks/",a="";t.length===0?a=`
            <div class="hero min-h-[400px] col-span-full">
                <div class="hero-content text-center mx-auto">
                    <div class="max-w-md">
                        <i class="fa-solid fa-palette text-6xl text-base-content mb-4"></i>
                        <h2 class="text-3xl font-bold">No artworks found.</h2>
                        <p class="py-6 text-base-content/70">Try adjusting your filters or search terms to find what you're looking for.</p>
                        <a href="${i}" class="clear-filters btn btn-primary">
                        <i class="fa-solid fa-refresh"></i> Clear Filters
                        </a>
                    </div>
                </div>
            </div>`:t.forEach(n=>{let r="",o=n.image_public_id,c=n.image_url,m=n.image_alt_text||n.name;c&&c.trim()&&c!=="/media/"?r=`<figure class="w-full"><img src="${c}" alt="${m}" class="w-full h-64 object-cover" loading="lazy"></figure>`:o&&s&&typeof getCloudinaryUrl<"u"?r=`<figure class="w-full"><img src="${getCloudinaryUrl(o,"w_400,h_300,c_fill,f_auto,q_auto")}" alt="${m}" class="w-full h-64 object-cover" loading="lazy"></figure>`:r='<figure class="w-full"><img src="/media/site_assets/noimage.png" alt="Placeholder" class="w-full h-64 object-cover"></figure>';let p="#",g="Unknown Artist";n.artist&&n.artist.username&&(p=`${typeof ARTWORK_LIST_URL<"u"?ARTWORK_LIST_URL:"/artworks/"}?artist=${n.artist.username}`,g=n.artist.username);let A=n.artist&&n.artist.username?`<p class="text-sm -mt-2 mb-2">
                             <a href="${p}" class="link link-hover">${g}</a>
                            </p>`:"",y=s&&n.slug?ARTWORK_DETAIL_BASE_PATH+n.slug+"/":"#",L=`
                <div class="card-body">
                    <h2 class="artwork-name card-title">${n.name}</h2>
                    ${A}
                    <p class="artwork-description">${n.description}</p>
                    <div class="divider my-2"></div>
                    <p class="artwork-price text-2xl font-bold text-primary">\xA3${n.price.toFixed(2)}</p>
                    
                    <div class="card-actions justify-between items-center mt-4">
                        ${n.is_in_stock?`
                            <button class="add-to-cart btn btn-primary btn-sm">
                                <i class="fa-solid fa-cart-plus"></i> Add to Cart
                            </button>
                            <a href="${y}" class="btn btn-outline btn-sm"><i class="fa-solid fa-eye"></i> Details</a>
                        `:`
                            <span class="sold-out badge badge-error">Sold Out</span>
                            <a href="${y}" class="btn btn-outline btn-sm"><i class="fa-solid fa-eye"></i> Details</a>
                        `}
                    </div>
                </div>`;a+=`<div class="artwork-card card shadow-xl hover:shadow-2xl transition-shadow" data-sku="${n.sku}">${r}${L}</div>`}),e.innerHTML=a}function k(t){return t.filter(e=>e.is_available||e.is_in_stock)}function h(t){return[...t].sort((e,s)=>e.price-s.price)}function S(t){return[...t].sort((e,s)=>s.price-e.price)}function x(t){return[...t].sort((e,s)=>e.name.localeCompare(s.name))}function R(t){return[...t].sort((e,s)=>{let i=e.artist?.username||e.name,a=s.artist?.username||s.name;return i.localeCompare(a)})}var u=[],l="price",d="asc",v=!1;function b(){let t=[...u];switch(l){case"price":t=d==="desc"?S(t):h(t);break;case"name":t=x(t);break;case"artist":t=R(t);break;default:t=h(t)}w(t)}function f(){document.querySelectorAll('.sort-control[data-type="sort"]').forEach(t=>{let e=t.getAttribute("data-sort-key"),s=t.getAttribute("data-sort-direction");String(e)===String(l)&&String(s)===String(d)?t.classList.add("btn-active"):t.classList.remove("btn-active")})}function T(t){let e=t.target.closest(".sort-control");if(!e||e.dataset.type!=="sort"||!v||u.length===0)return;t.preventDefault();let s=e.dataset.sortKey,i=e.dataset.sortDirection;l=s,d=i,f(),b();let a=new URL(window.location);a.searchParams.set("sort",s),a.searchParams.set("direction",i),window.history.pushState({},"",a)}function E(){let t=new URLSearchParams(window.location.search);l=t.get("sort")||"price",d=t.get("direction")||"asc",f()}function U(){if(E(),f(),typeof window.ARTWORKS_JSON_DATA<"u"&&window.ARTWORKS_JSON_DATA.length>0){u=window.ARTWORKS_JSON_DATA,v=!0;let e=new URLSearchParams(window.location.search);(e.has("sort")||e.has("direction"))&&b()}let t=document.getElementById("controls");t&&t.addEventListener("click",T)}function $(){let t=document.getElementById("min_price"),e=document.getElementById("max_price"),s=document.getElementById("apply-filters"),i=s?.closest("form");if(!t||!e||!s||!i)return;function a(){let n=parseFloat(t.value)||0,r=parseFloat(e.value)||0;t.value&&e.value&&n>r?(s.disabled=!0,s.title="Min price cannot be greater than max price",s.classList.add("btn-disabled")):(s.disabled=!1,s.title="",s.classList.remove("btn-disabled"))}t.addEventListener("change",a),t.addEventListener("input",a),e.addEventListener("change",a),e.addEventListener("input",a),i.addEventListener("submit",function(n){let r=parseFloat(t.value)||0,o=parseFloat(e.value)||0;t.value&&e.value&&r>o&&(n.preventDefault(),alert("Min price cannot be greater than max price"))}),a()}document.addEventListener("DOMContentLoaded",function(){U(),$()});})();
