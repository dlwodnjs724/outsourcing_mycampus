String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k])
    }
    return a
};

function createComponents(next_posts, status, callback) {

    var components = next_posts.map(function (post, idx) {
          var component = makeComponent(post.ctgy.name, post.name)
        }
    )
}
