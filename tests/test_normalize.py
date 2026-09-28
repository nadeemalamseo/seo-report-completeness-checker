from seo_report_checker.normalize import is_weak_text, looks_like_url
def test_url():
    assert looks_like_url("https://example.com/a") and not looks_like_url("example.com/a")
def test_weak_text():
    assert is_weak_text("Improve SEO") and not is_weak_text("The page has no unique title element.")
