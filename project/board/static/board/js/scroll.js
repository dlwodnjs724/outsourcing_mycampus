String.prototype.format = function (...content) {
    a = this;
    for (k in content) {
        a = a.replace("{" + k + "}", content[k])
    }
    return a
};

var componentTemplate = `
    <li class="board__post__container">
        <div class="board__post__content">
            <div class="post__text">
                <div class="post__top">
                    <div class="post__top__category">
                        {0}
                    </div>
                    <div class="post__top__author">
                        {1}
                    </div>
                </div>
                <div class="post__mid">
                    <div class="post__mid__title">
                        <a href="{2}">{3}</a>
                    </div>
                    <div class="post__mid__content">
                        {4}
                    </div>
                </div>
                <hr/>
                <div class="post__bottom">
                    <div class="post__bottom__icon">
                        <div class="s_con post__bottom__view">
                            <img src="{5}"/>
                            <span>{6}</span>
                        </div>
                        <div class="s_con post__bottom__like">
                            <button type="button" class="like" name="{7}" value="Like">
                                    <img id="m_like_id_{8}" class='{9}' src="{10}"/>
                            </button>
                            <span id="m_post_{11}">{12}</span>
                        </div>

                        <div class="s_con post__bottom__comment">
                            <img src="{13}"/>
                            <span>{14}</span>
                        </div>
                    </div>
                    <div class="post__bottom__right">
                        <div class="post__bottom__time">
                            {15}
                        </div>
                        <div class="post__bottom__bookmark">
                            <img src="{16}"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>
`;

