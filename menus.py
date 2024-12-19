import ffr_client as ffrc

main_menu_options = [
    {"text":"re-cord existing stream","func":ffrc.stream_record_start},
    {"text":"stop re-cording existing stream","func":ffrc.stream_record_stop},
    {"text":"Listen to existing stream","func":ffrc.stream_play},
    {"text":"Add new stream","func":ffrc.stream_add},
    {"text":"Remove stream","func":ffrc.stream_remove},
    {"text":"Edit existing stream","func":ffrc.stream_edit}
]

record_menu_options = [
        {"text":"re-cord now","func":ffrc.stream_record_start_now},
        {"text":"re-cord later","func":ffrc.stream_record_start_later}
    ]