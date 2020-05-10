package serenity.features.search;

import net.serenitybdd.core.annotations.findby.FindBy;
import net.serenitybdd.core.pages.WebElementFacade;
import net.serenitybdd.junit.runners.SerenityParameterizedRunner;
import net.serenitybdd.junit.runners.SerenityRunner;
import net.thucydides.core.annotations.Managed;
import net.thucydides.core.annotations.ManagedPages;
import net.thucydides.core.annotations.Steps;
import net.thucydides.core.pages.Pages;
import net.thucydides.junit.annotations.Qualifier;
import net.thucydides.junit.annotations.UseTestDataFrom;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.WebDriver;
import serenity.steps.serenity.EmagSteps;
import serenity.steps.serenity.EndUserSteps;

/**
 * @author joj on 5/10/2020
 **/

@RunWith(SerenityParameterizedRunner.class)
@UseTestDataFrom("src/test/resources/EmagTestData.csv")
public class EmagWebAutomationTest {

    @Managed(uniqueSession = true)
    public WebDriver webdriver;

    @ManagedPages(defaultUrl = "https://www.emag.ro/")
    public Pages pages;

    public String name;
    public String definition;

    @Qualifier
    public String getQualifier() {
        return name;
    }

    @Steps
    public EmagSteps endUser;

    @Test
    public void searchWikiByKeywordTestDDT() {
        endUser.is_the_home_page();
        endUser.looks_for(getName());
        endUser.should_see_definition(getDefinition());
    }

    @Test
    public void filterTestDdt() throws InterruptedException {
        endUser.is_the_home_page();
        endUser.looks_for(getName());
        endUser.check_filter_not_applied();
        endUser.filter_for();
        endUser.check_filter_applied();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDefinition() {
        return definition;
    }

    public void setDefinition(String definition) {
        this.definition = definition;
    }
}
