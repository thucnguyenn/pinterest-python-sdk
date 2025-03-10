"""
High level module class for Customer List object
"""
from __future__ import annotations


from pinterest.generated.client.api.customer_lists_api import CustomerListsApi

from pinterest.generated.client.model.user_list_type import UserListType
from pinterest.generated.client.model.customer_list_request import CustomerListRequest
from pinterest.generated.client.model.customer_list import CustomerList as GeneratedCustomerList
from pinterest.generated.client.model.customer_list_update_request import CustomerListUpdateRequest

from pinterest.client import PinterestSDKClient
from pinterest.utils.base_model import PinterestBaseModel
from pinterest.utils.error_handling import verify_api_response


class CustomerList(PinterestBaseModel):
    # pylint: disable=too-few-public-methods
    """
    High level model class to manage customer_lists for an CustomerList
    """
    def __init__(self, ad_account_id, customer_list_id, client=None, **kwargs):
        PinterestBaseModel.__init__(
            self,
            _id=str(customer_list_id),
            generated_api=CustomerListsApi,
            generated_api_get_fn="customer_lists_get",
            generated_api_get_fn_args={"ad_account_id": ad_account_id, "customer_list_id": customer_list_id},
            model_attribute_types = GeneratedCustomerList.openapi_types,
            client=client,
            )
        self._ad_account_id = str(ad_account_id)
        self._populate_fields(**kwargs)

    @classmethod
    def create(
        cls,
        ad_account_id : str,
        name : str,
        records : str,
        list_type : str = "EMAIL",
        client: PinterestSDKClient = None,
        **kwargs
    ):
        # pylint: disable=too-many-arguments
        """
        Create a customer list from your records(hashed or plain-text email addresses, or hashed MAIDs or IDFAs).

        A customer list is one of the four types of Pinterest audiences: for more information, see <a href="https://help.pinterest.com/en/business/article/audience-targeting">Audience targeting</a>
        or the <a href="https://developers.pinterest.com/docs/features/ads-management/#Audiences">Audiences</a> section of the ads management guide.

        Please review our <a href="https://help.pinterest.com/en/business/article/audience-targeting#section-13341">requirements</a> for what type of information is allowed when uploading a customer list.

        When you create a customer list, the system scans the list for existing Pinterest accounts; the list
        must include at least 100 Pinterest accounts. Your original list will be deleted when the matching process
        is complete. The filtered list – containing only the Pinterest accounts that were included in your starting
        list – is what will be used to create the audience.

        Note that once you have created your customer list, you must convert it into an audience
        (of the “CUSTOMER_LIST” type) using the <a href="https://developers.pinterest.com/docs/api/v5/#operation/create_audience_handler">create audience endpoint</a> before it can be used.


        Args:
            ad_account_id (str): Unique identifier of an ad account.
            name (str): Customer list name.
            records (str): Records list. Can be any combination of emails, MAIDs, or IDFAs. Emails must be lowercase
                    and can be plain text or hashed using SHA1, SHA256, or MD5. MAIDs and IDFAs must be hashed with SHA1, SHA256, or MD5.
            list_type (str, optional): User list type. Possible Enum: "EMAIL" "IDFA" "MAID" "LR_ID" "DLX_ID" "HASHED_PINNER_ID". Defaults to "EMAIL".
            client (PinterestSDKClient, optional): Defaults to default_api_client.

        Keyword Args:
            Any valid keyword arguments or query parameters for endpoint.

        Returns:
            CustomerList: CustomerList object
        """# pylint: disable=line-too-long

        UserListType(list_type)

        if not client:
            client = cls._get_client()

        api_response = CustomerListsApi(client).customer_lists_create(
            ad_account_id=str(ad_account_id),
            customer_list_request=CustomerListRequest(
                ad_account_id = str(ad_account_id),
                name = name,
                records = records,
                list_type = list_type,
                **kwargs
                ),
            )

        return CustomerList(
            ad_account_id=api_response.ad_account_id,
            customer_list_id=api_response.id,
            client=client
            )

    def update_fields(self, **kwargs):
        """
        Update customer lists fields with valid values

        Keywords Args:
            Any valid customer list field with valid value
        """
        api_response = self._generated_api.customer_lists_update(
            ad_account_id=self._ad_account_id,
            customer_list_id=self._id,
            customer_list_update_request=CustomerListUpdateRequest(
                **kwargs
            )
        )

        assert isinstance(api_response, GeneratedCustomerList)
        self._populate_fields()

        return True

    @classmethod
    def get_all(
        cls,
        ad_account_id: str,
        page_size: int = None,
        order: str = None,
        bookmark: str = None,
        client: PinterestSDKClient = None,
        **kwargs
    ) -> tuple[list[CustomerList], str]:
        # pylint: disable=too-many-arguments
        # pylint: disable=fixme
        """
        Get a list of the customer lists in the AdAccount, filtered by the specified arguments

        Args:
            ad_account_id (str): Campaign's Ad Account ID.
            page_size (int, optional): Maximum number of items to include in a single page of the response.
                                    See documentation on Pagination for more information. Defaults to None which will
                                    return default page size customer lists.
            order (str, optional): _description_. Defaults to None.
            bookmark (str, optional): Cursor used to fetch the next page of items. Defaults to None.
            client (PinterestSDKClient, optional): PinterestSDKClient Object

        Keyword Args:
            Any valid keyword arguments or query parameters for endpoint.

        Returns:
            list[CustomerList]: List of CustomerList Objects
            str: Bookmark for pagination if present, else None.
        """
        if page_size:
            kwargs["page_size"] = page_size
        if order:
            kwargs["order"] = order
        if bookmark:
            kwargs["bookmark"] = bookmark

        raw_customer_lists = []
        return_bookmark = None

        if not client:
            client = cls._get_client()

        customer_list_api = CustomerListsApi(api_client=client)
        api_response = customer_list_api.customer_lists_list(
            ad_account_id=ad_account_id,
            **kwargs
        )
        verify_api_response(api_response)

        raw_customer_lists += api_response.get("items")
        return_bookmark = api_response.get("bookmark")

        if len(raw_customer_lists) == 0:
            return None, None

        customer_lists = [
            CustomerList(
                ad_account_id=ad_account_id,
                customer_list_id=customer_list.get("id"),
                client=client,
                _model_data=customer_list,
            )
            for customer_list in raw_customer_lists
        ]

        return customer_lists, return_bookmark

    def add_record(self, record):
        """
        Add records to an existing customer list, the system scans the additions for existing Pinterest accounts; those
        are the records that will be added to your “CUSTOMER_LIST” audience.

        Your original list of records to add will be deleted when the matching process is complete.

        Args:
            record (str): Records list. Can be any combination of emails, MAIDs, or IDFAs. Emails must be
            lowercase and can be plain text or hashed using SHA1, SHA256, or MD5. MAIDs and IDFAs must be hashed with
            SHA1, SHA256, or MD5.

        Returns:
            bool: If record was added to the customer list fields were successfully updated
        """

        return self.update_fields(
            records=record,
            operation_type='ADD'
        )

    def remove_record(self, record):
        """
        Remove records to an existing customer list.

        Args:
            record (str): Records list. Can be any combination of emails, MAIDs, or IDFAs. Emails must be
            lowercase and can be plain text or hashed using SHA1, SHA256, or MD5. MAIDs and IDFAs must be hashed with
            SHA1, SHA256, or MD5.

        Returns:
            bool: If record was removed to the customer list fields were successfully updated
        """

        return self.update_fields(
            records=record,
            operation_type='REMOVE'
        )
