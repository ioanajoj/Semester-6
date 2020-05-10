package serenity.pages;

import net.serenitybdd.core.annotations.findby.By;
import net.serenitybdd.core.annotations.findby.FindBy;
import net.serenitybdd.core.pages.WebElementFacade;
import net.thucydides.core.annotations.DefaultUrl;
import net.thucydides.core.pages.PageObject;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Action;
import org.openqa.selenium.interactions.Actions;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * @author joj on 5/10/2020
 **/

@DefaultUrl("https://www.emag.ro/")
public class EmagResultPage extends PageObject {

    @FindBy(name="query")
    private WebElementFacade searchTerms;

    @FindBy(className = "searchbox-submit-button")
    private WebElementFacade lookupButton;

    @FindBy(id = "js-filter-6407-collapse")
    private WebElementFacade stoc;

    @FindBy(id = "js-filter-6411-collapse")
    private WebElementFacade pret;

    @FindBy(className = "listing-grid-group-scroller-inner")
    private WebElementFacade filterScroller;

    public void filter() {
        Optional<WebElement> filter1 = stoc.findElements(By.tagName("a")).stream().findFirst();
        evaluateJavascript("arguments[0].scrollIntoView();", filter1.get());
        evaluateJavascript("window.scrollBy(0,-70);");
        filter1.get().click();
        Optional<WebElement> filter2 = pret.findElements(By.tagName("a")).stream().findFirst();
        evaluateJavascript("arguments[0].scrollIntoView();", filter2.get());
        evaluateJavascript("window.scrollBy(0,-70);");
        filter2.get().click();
    }

    public void check_filter_not_applied() {
        assert find(By.className("listing-active-filters-holder")).getTextContent().contains("Nu au fost aplicate filtre");
    }

    public void check_filter_applied() throws InterruptedException {
        assert find(By.className("remove-search-word-button")) != null;
    }

    public void enter_keywords(String keyword) {
        searchTerms.type(keyword);
    }

    public void lookup_terms() {
        lookupButton.click();
    }

    public List<String> getDefinitions() {
        WebElementFacade definitionList = find(By.className("js-products-container"));
        return definitionList.findElements(By.className("js-product-data")).stream()
                .map( element -> element.getText() )
                .collect(Collectors.toList());
    }
}



