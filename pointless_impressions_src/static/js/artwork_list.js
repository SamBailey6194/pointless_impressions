(()=>{function S(e){let t=document.getElementById("artwork-list");if(!t)return;let s=typeof getCloudinaryUrl<"u"&&typeof ARTWORK_DETAIL_BASE_PATH<"u",n=typeof ARTWORK_LIST_URL<"u"?ARTWORK_LIST_URL:"/artworks/",r="";e.length===0?r=`
            <div class="hero min-h-[400px] col-span-full">
                <div class="hero-content text-center mx-auto">
                    <div class="max-w-md">
                        <i class="fa-solid fa-palette text-6xl text-base-content mb-4"></i>
                        <h2 class="text-3xl font-bold">No artworks found.</h2>
                        <p class="py-6 text-base-content/70">Try adjusting your filters or search terms to find what you're looking for.</p>
                        <a href="${n}" class="clear-filters btn btn-primary">
                        <i class="fa-solid fa-refresh"></i> Clear Filters
                        </a>
                    </div>
                </div>
            </div>`:e.forEach(i=>{let a="",o=i.image_public_id,c=i.image_url,m=i.image_alt_text||i.name;c&&c.trim()&&c!=="/media/"?a=`<figure class="w-full"><img src="${c}" alt="${m}" class="w-full h-64 object-cover" loading="lazy"></figure>`:o&&s&&typeof getCloudinaryUrl<"u"?a=`<figure class="w-full"><img src="${getCloudinaryUrl(o,"w_400,h_300,c_fill,f_auto,q_auto")}" alt="${m}" class="w-full h-64 object-cover" loading="lazy"></figure>`:a='<figure class="w-full"><img src="/media/site_assets/noimage.png" alt="Placeholder" class="w-full h-64 object-cover"></figure>';let p="#",g="Unknown Artist";i.artist&&i.artist.user_profile&&i.artist.user_profile.user&&i.artist.user_profile.user.username&&(p=`${typeof ARTWORK_LIST_URL<"u"?ARTWORK_LIST_URL:"/artworks/"}?artist=${i.artist.user_profile.user.username}`,g=i.artist.user_profile.user.username);let b=i.artist&&i.artist.user_profile&&i.artist.user_profile.user&&i.artist.user_profile.user.username?`<p class="text-sm -mt-2 mb-2">
                             <a href="${p}" class="link link-hover">${g}</a>
                            </p>`:"",y=s&&i.slug?ARTWORK_DETAIL_BASE_PATH+i.slug+"/":"#",A=`
                <div class="card-body">
                    <h2 class="artwork-name card-title">${i.name}</h2>
                    ${b}
                    <p class="artwork-description">${i.description}</p>
                    <div class="divider my-2"></div>
                    <p class="artwork-price text-2xl font-bold text-primary">\xA3${i.price.toFixed(2)}</p>
                    
                    <div class="card-actions justify-between items-center mt-4">
                        ${i.is_in_stock?`
                            <a href="${y}" class="btn btn-outline btn-sm ml-auto">
                                <i class="fa-solid fa-eye"></i> Details
                            </a>
                        `:`
                            <span class="sold-out badge badge-error">Sold Out</span>
                            <a href="${y}" class="btn btn-outline btn-sm">
                                <i class="fa-solid fa-eye"></i> Details
                            </a>
                        `}
                    </div>
                </div>`;r+=`<div class="artwork-card card shadow-xl hover:shadow-2xl transition-shadow" data-sku="${i.sku}">${a}${A}</div>`}),t.innerHTML=r}function B(e){return e.filter(t=>t.is_available||t.is_in_stock)}function h(e){return[...e].sort((t,s)=>t.price-s.price)}function x(e){return[...e].sort((t,s)=>s.price-t.price)}function w(e){return[...e].sort((t,s)=>t.name.localeCompare(s.name))}function R(e){return[...e].sort((t,s)=>{let n=t.artist?.username||t.name,r=s.artist?.username||s.name;return n.localeCompare(r)})}var u=[],l="price",d="asc",v=!1;function _(){let e=[...u];switch(l){case"price":e=d==="desc"?x(e):h(e);break;case"name":e=w(e);break;case"artist":e=R(e);break;default:e=h(e)}S(e)}function f(){document.querySelectorAll('.sort-control[data-type="sort"]').forEach(e=>{let t=e.getAttribute("data-sort-key"),s=e.getAttribute("data-sort-direction");String(t)===String(l)&&String(s)===String(d)?e.classList.add("btn-active"):e.classList.remove("btn-active")})}function T(e){let t=e.target.closest(".sort-control");if(!t||t.dataset.type!=="sort"||!v||u.length===0)return;e.preventDefault();let s=t.dataset.sortKey,n=t.dataset.sortDirection;l=s,d=n,f(),_();let r=new URL(window.location);r.searchParams.set("sort",s),r.searchParams.set("direction",n),window.history.pushState({},"",r)}function E(){let e=new URLSearchParams(window.location.search);l=e.get("sort")||"price",d=e.get("direction")||"asc",f()}function U(){if(E(),f(),typeof window.ARTWORKS_JSON_DATA<"u"&&window.ARTWORKS_JSON_DATA.length>0){u=window.ARTWORKS_JSON_DATA,v=!0;let t=new URLSearchParams(window.location.search);(t.has("sort")||t.has("direction"))&&_()}let e=document.getElementById("controls");e&&e.addEventListener("click",T)}function $(){let e=document.getElementById("min_price"),t=document.getElementById("max_price"),s=document.getElementById("apply-filters"),n=s?.closest("form");if(!e||!t||!s||!n)return;function r(){let i=parseFloat(e.value)||0,a=parseFloat(t.value)||0;e.value&&t.value&&i>a?(s.disabled=!0,s.title="Min price cannot be greater than max price",s.classList.add("btn-disabled")):(s.disabled=!1,s.title="",s.classList.remove("btn-disabled"))}e.addEventListener("change",r),e.addEventListener("input",r),t.addEventListener("change",r),t.addEventListener("input",r),n.addEventListener("submit",function(i){let a=parseFloat(e.value)||0,o=parseFloat(t.value)||0;e.value&&t.value&&a>o&&(i.preventDefault(),alert("Min price cannot be greater than max price"))}),r()}document.addEventListener("DOMContentLoaded",function(){U(),$()});})();
