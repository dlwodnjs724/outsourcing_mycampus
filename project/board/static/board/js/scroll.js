String.prototype.format = function (...content) {
    a = this;
    for (k in content) {
        a = a.replace("{" + k + "}", content[k])
    }
    return a
};

String.prototype.replaceAll = function (org, dest) {
    return this.split(org).join(dest);
};

String.prototype.formatFromObj = function (ctx) {
    a = this;
    for (k of Object.keys(ctx)) {
        a = a.replaceAll("{" + k + "}", ctx[k]);
    }

    return a;
};

var componentTemplate = `
    <li class="board__post__container">
        <div class="board__post__like">
            <span id="post_{0}">{1}</span>
            <button type="button" class="like" name="{2}" value="Like"
                    onclick="likePost({3})">
                <img id="like_id_{4}" class='{5}' src="{6}"/>
            </button>
        </div>
        <div class="board__post__content">
            <div class="post__text">
                <div class="post__top">
                    <div class="post__top__category">
                        {7}
                    </div>
                    <div class="post__top__author">
                        {8}
                    </div>
                </div>
                <div class="post__mid">
                    <div class="post__mid__title">
                        <a href="{9}">{10}</a>
                    </div>
                    <div class="post__mid__content">
                        {11}
                    </div>
                </div>
                <hr/>
                <div class="post__bottom">
                    <div class="post__bottom__icon">
                        <div class="s_con post__bottom__view">
                            <img src="{12}"/>
                            <span>{13}</span>
                        </div>
                        <div class="s_con post__bottom__comment">
                            <img src="{14}"/>
                            <span>{15}</span>
                        </div>
                        <div class="s_con post__bottom__bookmark">
                            <img src="{16}"/>
                            <span>{17}</span>
                        </div>
                    </div>
                    <div class="post__bottom__time">
                        {18}
                    </div>
                </div>
            </div>

            <div class="post__image">
                <img src="{19}" alt="">
            </div>
        </div>
    </li>
`;

var mobileTemplate = `
    <li class="board__post__container">
        <div class="board__post__content">
            <div class="post__text">
                <div class="post__top">
                    <div class="post__top__category">
                        {post.ctgy.name}
                    </div>
                    <div class="post__top__author">
                        {post.name}
                    </div>
                </div>
                <div class="post__mid">
                    <div class="post__mid__title">
                        <a href="{detailUrl}">{post.title}</a>
                    </div>
                    <div class="post__mid__content">
                        {post.content}
                    </div>
                </div>
                <hr/>
                <div class="post__bottom">
                    <div class="post__bottom__icon">
                        <div class="s_con post__bottom__view">
                                <img src="{view_icon_will_use}"/>
                            
                            <span>{post.views}</span>
                        </div>

                        <div class="s_con post__bottom__like">
                            <button type="button" class="like" name="{post.pk}" value="Like"
                                    onclick="likePost({post.pk})">
                                    <img id="m_like_id_{post.pk}" class='{isClicked}'
                                         src="{like_icon_will_use}"/>
                            </button>
                            <span id="m_post_{post.pk}">{post.total_likes}</span>
                        </div>

                        <div class="s_con post__bottom__comment">
                                <img src="{comment_icon_will_use}"/>
                            <span>{post.comments.all.count}</span>
                        </div>
                    </div>
                    <div class="post__bottom__right">
                        <div class="post__bottom__time">
                            {post.time_interval}
                        </div>
                        <div class="post__bottom__bookmark">
                            <img src="{save_icon_will_use}"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>
`