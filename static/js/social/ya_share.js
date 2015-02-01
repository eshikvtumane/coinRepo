// создаем блок
function ya_share(usr_title, usr_link){}
        return new Ya.share({
        element: 'ya_share',
            elementStyle: {
                'type': 'button',
                'border': true,
                'quickServices': ['lj', 'twitter', '|', 'vkontakte']
            },
            link: usr_link,
            title: usr_title,
            popupStyle: {
                blocks: {
                    'Поделись-ка!': ['vkontakte', 'twitter', 'evernote', 'lj' ],
                    'Поделись-ка по-другому!': ['lj', 'twitter', 'vkontakte']
                },
                copyPasteField: true
            }
});
