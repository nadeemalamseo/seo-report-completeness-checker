from seo_report_checker.normalize import clean, is_weak_text, looks_like_url


def test_url():
    assert looks_like_url("https://example.com/a")
    assert not looks_like_url("example.com/a")


def test_url_rejects_credentials_whitespace_and_invalid_ports():
    for value in (
        "https://user:pass@example.com/path",
        "https://example.com:99999/path",
        "https://example.com:bad/path",
        " https://example.com/path",
        "https://example.com/a b",
        "https://exa_mple.com/",
        "https://999.999.999.999/",
    ):
        assert not looks_like_url(value), value


def test_url_accepts_ipv4_ipv6_idn_and_localhost():
    assert looks_like_url("http://127.0.0.1:8080/")
    assert looks_like_url("https://[2001:db8::1]/")
    assert looks_like_url("https://xn--bcher-kva.example/")
    assert looks_like_url("http://localhost:3000/")


def test_weak_text():
    assert is_weak_text("Improve SEO")
    assert not is_weak_text("The page has no unique title element.")


def test_clean_preserves_zero_and_false():
    assert clean(0) == "0"
    assert clean(False) == "False"
